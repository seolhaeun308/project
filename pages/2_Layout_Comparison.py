# pages/2_Layout_Comparison.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="2. 집중 vs 분산 비교", layout="wide")
st.title("2️⃣ 집중 vs 분산 배치 구조 최적화 (3D)")

def calculate_heat_diffuse(grid, alpha, time_steps, hotspots, hotspot_temp):
    new_grid = grid.copy()
    for step in range(time_steps):
        new_grid[1:-1, 1:-1] = grid[1:-1, 1:-1] + alpha * (grid[:-2, 1:-1] + grid[2:, 1:-1] + grid[1:-1, :-2] + grid[1:-1, 2:] - 4 * grid[1:-1, 1:-1])
        grid = new_grid.copy()
        for (x, y) in hotspots:
            grid[y, x] = hotspot_temp
    return grid

def plot_3d_surface(grid, title_text):
    fig = go.Figure(data=[go.Surface(z=grid, colorscale='Inferno')])
    fig.update_layout(title=title_text, scene=dict(zaxis=dict(range=[25, 120])))
    return fig

grid_size = st.sidebar.slider("격자 크기", 20, 100, 40)
hotspot_temp = st.sidebar.slider("핫스팟 초기 온도", 50, 150, 100)
time_steps = st.sidebar.slider("시간 흐름 (Steps)", 1, 500, 200)

if st.button("⚖️ 방열 효과 비교하기"):
    center = grid_size // 2
    offset = grid_size // 4
    init_grid = np.ones((grid_size, grid_size)) * 25.0
    
    # 모델 A (집중)
    grid_A = calculate_heat_diffuse(init_grid.copy(), 0.10, time_steps, [(center, center)], hotspot_temp)
    # 모델 B (분산)
    grid_B = calculate_heat_diffuse(init_grid.copy(), 0.10, time_steps, 
                                   [(center-offset, center-offset), (center-offset, center+offset), 
                                    (center+offset, center-offset), (center+offset, center+offset)], hotspot_temp)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_3d_surface(grid_A, "Concentrated Hotspot"), use_container_width=True)
    with col2:
        st.plotly_chart(plot_3d_surface(grid_B, "Distributed Hotspots"), use_container_width=True)

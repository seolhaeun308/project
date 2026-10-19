# pages/3_TSV_Optimization.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="3. TSV 최적화", layout="wide")
st.title("3️⃣ 이종 소재(TSV 방열 기둥) 적용 시뮬레이션")

def calculate_heat_diffuse(grid, alpha_map, time_steps, hotspots, hotspot_temp):
    new_grid = grid.copy()
    inner_alpha = alpha_map[1:-1, 1:-1]
    for step in range(time_steps):
        new_grid[1:-1, 1:-1] = grid[1:-1, 1:-1] + inner_alpha * (grid[:-2, 1:-1] + grid[2:, 1:-1] + grid[1:-1, :-2] + grid[1:-1, 2:] - 4 * grid[1:-1, 1:-1])
        grid = new_grid.copy()
        for (x, y) in hotspots:
            grid[y, x] = hotspot_temp
    return grid

def plot_3d_surface(grid, title_text):
    fig = go.Figure(data=[go.Surface(z=grid, colorscale='Inferno')])
    fig.update_layout(title=title_text, scene=dict(zaxis=dict(range=[25, 120])))
    return fig

grid_size = st.sidebar.slider("격자 크기", 20, 100, 40)
tsv_alpha = st.sidebar.slider("TSV 열전도율 (Copper)", 0.15, 0.25, 0.24)

if st.button("⚖️ 일반 실리콘 vs TSV 칩 비교"):
    center = grid_size // 2; offset = 2
    hotspots = [(center, center)]
    init_grid = np.ones((grid_size, grid_size)) * 25.0
    
    # 모델 A (일반)
    alpha_map_A = np.ones((grid_size, grid_size)) * 0.10
    grid_A = calculate_heat_diffuse(init_grid.copy(), alpha_map_A, 200, hotspots, 100)
    
    # 모델 B (TSV)
    alpha_map_B = np.ones((grid_size, grid_size)) * 0.10
    for x, y in [(center-offset, center), (center+offset, center), (center, center-offset), (center, center+offset)]:
        alpha_map_B[y, x] = tsv_alpha
    grid_B = calculate_heat_diffuse(init_grid.copy(), alpha_map_B, 200, hotspots, 100)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_3d_surface(grid_A, "Standard Silicon"), use_container_width=True)
    with col2:
        st.plotly_chart(plot_3d_surface(grid_B, "Silicon with Cu TSV"), use_container_width=True)

import streamlit as st
import numpy as np
import plotly.graph_objects as go

def apply_space_theme():
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background: radial-gradient(circle at 15% 25%, rgba(60, 20, 80, 0.6) 0%, transparent 40%), linear-gradient(-45deg, #01010a, #0a0520, #010205); }
    [data-testid="stSidebar"] { background: rgba(5, 10, 25, 0.4) !important; backdrop-filter: blur(15px); }
    h1, p, span, div, label { color: #E6F1FF !important; }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="2. 집중 vs 분산 비교", layout="wide")
apply_space_theme()

st.title("2️⃣ 집중 vs 분산 배치 구조 최적화 (3D)")

def calculate_heat_diffuse(grid, alpha, time_steps, hotspots, hotspot_val):
    new_grid = grid.copy()
    
    # 💡 [핵심 수정] 발생할 '총 발열량'을 계산하고, 이를 핫스팟 개수로 똑같이 나눔 (에너지 보존 법칙)
    total_heat_power = (hotspot_val - 25.0) * 0.15
    power_per_spot = total_heat_power / len(hotspots) # 4곳이면 1/4씩 공급됨
    
    for step in range(time_steps):
        new_grid[1:-1, 1:-1] = grid[1:-1, 1:-1] + alpha * (grid[:-2, 1:-1] + grid[2:, 1:-1] + grid[1:-1, :-2] + grid[1:-1, 2:] - 4 * grid[1:-1, 1:-1])
        grid = new_grid.copy()
        
        # 핫스팟 위치에 열 에너지 가산
        for (x, y) in hotspots:
            grid[y, x] += power_per_spot
            
    return grid

def plot_3d_surface(grid, title_text):
    fig = go.Figure(data=[go.Surface(z=grid, colorscale='Inferno')])
    fig.update_layout(title=title_text, scene=dict(zaxis=dict(range=[25, 180])), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, b=0, t=40))
    return fig

grid_size = st.sidebar.slider("격자 크기", 20, 100, 40)
hotspot_val = st.sidebar.slider("총 발열 강도 (기준값)", 50, 150, 100)
time_steps = st.sidebar.slider("시간 흐름 (Steps)", 1, 500, 200)

if st.button("⚖️ 방열 효과 비교하기"):
    center = grid_size // 2
    offset = grid_size // 4
    init_grid = np.ones((grid_size, grid_size)) * 25.0
    
    grid_A = calculate_heat_diffuse(init_grid.copy(), 0.10, time_steps, [(center, center)], hotspot_val)
    grid_B = calculate_heat_diffuse(init_grid.copy(), 0.10, time_steps, 
                                   [(center-offset, center-offset), (center-offset, center+offset), 
                                    (center+offset, center-offset), (center+offset, center+offset)], hotspot_val)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_3d_surface(grid_A, "Concentrated Hotspot"), use_container_width=True)
        st.metric(label="모델 A 최고 온도 (집중)", value=f"{np.max(grid_A):.1f} °C") 
    with col2:
        st.plotly_chart(plot_3d_surface(grid_B, "Distributed Hotspots"), use_container_width=True)
        
        # 💡 에너지를 1/4씩 쪼갰으므로, 모델 B의 최고 온도가 무조건 떨어짐!
        delta_val = np.max(grid_B) - np.max(grid_A) 
        st.metric(label="모델 B 최고 온도 (분산)", value=f"{np.max(grid_B):.1f} °C", delta=f"{delta_val:.1f} °C (분산 방열 효과)", delta_color="inverse")

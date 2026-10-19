# pages/1_Single_Hotspot.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="1. 단일 핫스팟 3D", layout="wide")
st.title("1️⃣ 단일 핫스팟 3D 열 확산 시뮬레이션")

# 물리 엔진 핵심 함수들
def calculate_heat_diffuse(grid, alpha, time_steps, hotspots, hotspot_temp):
    try:
        new_grid = grid.copy()
        for step in range(time_steps):
            up = grid[:-2, 1:-1]; down = grid[2:, 1:-1]
            left = grid[1:-1, :-2]; right = grid[1:-1, 2:]
            center = grid[1:-1, 1:-1]
            new_grid[1:-1, 1:-1] = center + alpha * (up + down + left + right - 4 * center)
            grid = new_grid.copy()
            for (x, y) in hotspots:
                grid[y, x] = hotspot_temp
        return grid
    except Exception as e:
        st.error(f"오류: {e}")
        return grid

def plot_3d_surface(grid, title_text):
    fig = go.Figure(data=[go.Surface(z=grid, colorscale='Inferno')])
    fig.update_layout(title=title_text, scene=dict(zaxis=dict(range=[25, 120])))
    return fig

# UI 및 실행 로직
st.sidebar.header("⚙️ 시뮬레이션 설정")
grid_size = st.sidebar.slider("격자 크기", 20, 100, 40)
hotspot_temp = st.sidebar.slider("핫스팟 초기 온도", 50, 150, 100)
alpha = st.sidebar.slider("열전도율 (Alpha)", 0.01, 0.20, 0.10)
time_steps = st.sidebar.slider("시간 흐름 (Steps)", 1, 500, 200)

if st.button("▶️ 3D 시뮬레이션 시작"):
    with st.spinner('계산 중...'):
        initial_grid = np.ones((grid_size, grid_size)) * 25.0
        center = grid_size // 2
        hotspots = [(center, center)]
        final_grid = calculate_heat_diffuse(initial_grid, alpha, time_steps, hotspots, hotspot_temp)
        st.plotly_chart(plot_3d_surface(final_grid, "Single Hotspot (3D)"), use_container_width=True)

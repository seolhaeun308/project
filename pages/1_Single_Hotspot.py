# pages/1_Single_Hotspot.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

def apply_space_theme():
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background: radial-gradient(circle at 15% 25%, rgba(60, 20, 80, 0.6) 0%, transparent 40%), radial-gradient(circle at 75% 65%, rgba(20, 50, 100, 0.6) 0%, transparent 40%), linear-gradient(-45deg, #01010a, #0a0520, #010205); background-size: 200% 200%; animation: cosmicMove 15s ease infinite; }
    [data-testid="stAppViewContainer"]::before { content: ""; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-image: radial-gradient(1.5px 1.5px at 10% 20%, #ffffff, transparent), radial-gradient(2px 2px at 30% 60%, #aaccff, transparent), radial-gradient(1px 1px at 70% 40%, #ffffff, transparent), radial-gradient(1.5px 1.5px at 80% 90%, #aaccff, transparent), radial-gradient(2.5px 2.5px at 40% 10%, #ffffff, transparent), radial-gradient(1px 1px at 60% 80%, #ffffff, transparent); background-size: 150px 150px; opacity: 0.6; animation: twinkle 5s infinite alternate; pointer-events: none; z-index: 0; }
    [data-testid="stSidebar"] { background: rgba(5, 10, 25, 0.4) !important; backdrop-filter: blur(15px); border-right: 1px solid rgba(255, 255, 255, 0.1); }
    h1, h2, h3, p, span, div, label, li { color: #E6F1FF !important; text-shadow: 0px 0px 4px rgba(255,255,255,0.2); }
    @keyframes cosmicMove { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    @keyframes twinkle { 0% {opacity: 0.2;} 100% {opacity: 0.9;} }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="1. 단일 핫스팟 3D", layout="wide")
apply_space_theme() # 🌌 웅장한 우주 배경 실행!

st.title("1️⃣ 단일 핫스팟 3D 열 확산 시뮬레이션")

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
    fig.update_layout(title=title_text, scene=dict(zaxis=dict(range=[25, 120])), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

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

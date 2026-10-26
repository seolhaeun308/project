# pages/1_Single_Hotspot.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

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

st.set_page_config(page_title="1. 단일 핫스팟 3D 애니메이션", layout="wide")
apply_space_theme()

st.title("1️⃣ 단일 핫스팟 3D 열 확산 애니메이션")
st.write("유한차분법(FDM) 연산 과정이 시간 흐름에 따라 3D 표면상에서 어떻게 확산되는지 실시간 플레이어로 관찰합니다.")

# [최적화] @st.cache_data를 이용한 물리 연산 결과 캐싱
@st.cache_data
def run_full_simulation(grid_size, alpha, total_steps, hotspot_temp):
    grid = np.ones((grid_size, grid_size)) * 25.0
    center = grid_size // 2
    hotspots = [(center, center)]
    
    history = []
    current_grid = grid.copy()
    
    for step in range(total_steps):
        new_grid = current_grid.copy()
        up = current_grid[:-2, 1:-1]; down = current_grid[2:, 1:-1]
        left = current_grid[1:-1, :-2]; right = current_grid[1:-1, 2:]
        center_region = current_grid[1:-1, 1:-1]
        
        new_grid[1:-1, 1:-1] = center_region + alpha * (up + down + left + right - 4 * center_region)
        current_grid = new_grid.copy()
        
        for (x, y) in hotspots:
            current_grid[y, x] = hotspot_temp
            
        history.append(current_grid.copy())
    return history

def plot_3d_surface(grid, title_text):
    fig = go.Figure(data=[go.Surface(z=grid, colorscale='Inferno')])
    fig.update_layout(title=title_text, scene=dict(zaxis=dict(range=[25, 150])), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

st.sidebar.header("⚙️ 애니메이션 설정")
grid_size = st.sidebar.slider("격자 크기", 20, 60, 40)
hotspot_temp = st.sidebar.slider("핫스팟 초기 온도", 50, 150, 100)
alpha = st.sidebar.slider("열전도율 (Alpha)", 0.01, 0.20, 0.10)
total_steps = st.sidebar.slider("총 시뮬레이션 스텝", 20, 200, 100, step=10)

col_btn1, col_btn2 = st.columns(2)
start_animation = col_btn1.button("▶️ 열 확산 애니메이션 재생")

if start_animation:
    history_grids = run_full_simulation(grid_size, alpha, total_steps, hotspot_temp)
    
    # 실시간 갱신을 위한 빈 컨테이너 생성
    plot_placeholder = st.empty()
    progress_bar = st.progress(0)
    
    for i, grid_state in enumerate(history_grids):
        fig = plot_3d_surface(grid_state, f"Thermal Diffusion - Step {i+1}/{total_steps}")
        plot_placeholder.plotly_chart(fig, use_container_width=True)
        progress_bar.progress((i + 1) / total_steps)
        time.sleep(0.03) # 프레임 속도 조절
        
    st.success("✨ 열 확산 애니메이션 재생 완료!")

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

st.set_page_config(page_title="1. 단일 핫스팟 3D 최적화", layout="wide")
apply_space_theme()

st.title("1️⃣ 단일 핫스팟 3D 열 확산 애니메이션 (속도 최적화)")
st.write("넘파이(NumPy) 벡터 연산 최적화 및 렌더링 주기 조절을 통해 버벅임을 해결한 버전입니다.")

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
    fig.update_layout(title=title_text, scene=dict(zaxis=dict(range=[25, 150])), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, b=0, t=40))
    return fig

st.sidebar.header("⚙️ 애니메이션 설정")
grid_size = st.sidebar.slider("격자 크기 (해상도)", 20, 60, 40)
hotspot_temp = st.sidebar.slider("핫스팟 초기 온도", 50, 150, 100)
alpha = st.sidebar.slider("열전도율 (Alpha)", 0.01, 0.20, 0.10)
total_steps = st.sidebar.slider("총 시뮬레이션 스텝", 20, 200, 100, step=10)

if st.button("▶️ 최적화된 애니메이션 재생"):
    history_grids = run_full_simulation(grid_size, alpha, total_steps, hotspot_temp)
    
    plot_placeholder = st.empty()
    progress_bar = st.progress(0)
    
    # [최적화 핵심] 매 스텝마다 그리던 것을 2스텝마다 그리도록 건너뛰어 버벅임 대폭 감소
    skip_frames = 2 
    
    for i in range(0, len(history_grids), skip_frames):
        grid_state = history_grids[i]
        fig = plot_3d_surface(grid_state, f"Thermal Diffusion - Step {i+1}/{total_steps} (Optimized)")
        plot_placeholder.plotly_chart(fig, use_container_width=True)
        progress_bar.progress((i + 1) / total_steps)
        time.sleep(0.01)
        
    # 마지막 최종 스텝은 확실하게 보장
    plot_placeholder.plotly_chart(plot_3d_surface(history_grids[-1], f"Thermal Diffusion - Final Step"), use_container_width=True)
    progress_bar.progress(1.0)
    st.success("✨ 부드러운 최적화 재생 완료!")
    @st.cache_data
def run_full_simulation(grid_size, alpha, total_steps, hotspot_temp):
    grid = np.ones((grid_size, grid_size)) * 25.0 # 초기 상온(25도) 설정
    center = grid_size // 2
    hotspots = [(center, center)]
    
    history = []
    current_grid = grid.copy()
    
    for step in range(total_steps):
        new_grid = current_grid.copy()
        
        # 행렬 슬라이싱을 이용한 주변 노드(상, 하, 좌, 우) 온도 추출
        up = current_grid[:-2, 1:-1]; down = current_grid[2:, 1:-1]
        left = current_grid[1:-1, :-2]; right = current_grid[1:-1, 2:]
        center_region = current_grid[1:-1, 1:-1]
        
        # 유한차분법(FDM) 수식을 적용하여 현재 노드의 다음 스텝 온도 계산
        new_grid[1:-1, 1:-1] = center_region + alpha * (up + down + left + right - 4 * center_region)
        current_grid = new_grid.copy()
        
        # 디리클레 경계 조건: 트랜지스터 핫스팟의 발열 온도를 지속 유지
        for (x, y) in hotspots:
            current_grid[y, x] = hotspot_temp
            
        history.append(current_grid.copy())
    return history

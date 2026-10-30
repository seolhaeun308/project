# pages/2_Layout_Comparison.py
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

st.set_page_config(page_title="2. 집중 vs 분산 비교", layout="wide")
apply_space_theme()

st.title("2️⃣ 집중 vs 분산 배치 구조 최적화 (3D)")

# [핵심 로직] 유한차분법(FDM) 열 확산 함수 (재사용 모듈)
def calculate_heat_diffuse(grid, alpha, time_steps, hotspots, hotspot_temp):
    new_grid = grid.copy()
    
    # 시간 스텝(time_steps)에 따른 2차원 열전달 방정식 연산 (FDM)
    for step in range(time_steps):
        new_grid[1:-1, 1:-1] = grid[1:-1, 1:-1] + alpha * (grid[:-2, 1:-1] + grid[2:, 1:-1] + grid[1:-1, :-2] + grid[1:-1, 2:] - 4 * grid[1:-1, 1:-1])
        grid = new_grid.copy()
        
        # 디리클레 경계 조건 적용 (핫스팟 리스트에 포함된 모든 좌표의 온도를 지속 유지)
        for (x, y) in hotspots:
            grid[y, x] = hotspot_temp
    return grid

# [시각화 로직] 3D Surface 렌더링 함수 (재사용 모듈)
def plot_3d_surface(grid, title_text):
    fig = go.Figure(data=[go.Surface(z=grid, colorscale='Inferno')])
    fig.update_layout(title=title_text, scene=dict(zaxis=dict(range=[25, 120])), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

grid_size = st.sidebar.slider("격자 크기", 20, 100, 40)
hotspot_temp = st.sidebar.slider("핫스팟 초기 온도", 50, 150, 100)
time_steps = st.sidebar.slider("시간 흐름 (Steps)", 1, 500, 200)

if st.button("⚖️ 방열 효과 비교하기"):
    center = grid_size // 2
    offset = grid_size // 4
    init_grid = np.ones((grid_size, grid_size)) * 25.0
    
    # [함수 재사용] 모델 A: 발열원을 중앙 1곳에 집중 배치 (대조군)
    grid_A = calculate_heat_diffuse(init_grid.copy(), 0.10, time_steps, [(center, center)], hotspot_temp)
    
    # [함수 재사용] 모델 B: 동일한 열원을 4곳으로 분산 배치 (실험군)
    grid_B = calculate_heat_diffuse(init_grid.copy(), 0.10, time_steps, 
                                   [(center-offset, center-offset), (center-offset, center+offset), 
                                    (center+offset, center-offset), (center+offset, center+offset)], hotspot_temp)

    # 두 모델의 방열 효율 결과를 좌우로 배치하여 시각적으로 비교 분석
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_3d_surface(grid_A, "Concentrated Hotspot"), use_container_width=True)
    with col2:
        st.plotly_chart(plot_3d_surface(grid_B, "Distributed Hotspots"), use_container_width=True)
# 두 모델의 방열 효율 결과를 좌우로 배치하여 시각적으로 비교 분석
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_3d_surface(grid_A, "Concentrated Hotspot"), use_container_width=True)
        # 💡 추가: 수치 데이터 비교 (최고 온도 표시)
        st.metric(label="모델 A 최고 온도", value=f"{np.max(grid_A):.1f} °C") 
    with col2:
        st.plotly_chart(plot_3d_surface(grid_B, "Distributed Hotspots"), use_container_width=True)
        # 💡 추가: 수치 데이터 비교 (모델 A 대비 얼마나 온도가 낮아졌는지 시각화)
        temp_diff = np.max(grid_B) - np.max(grid_A)
        st.metric(label="모델 B 최고 온도", value=f"{np.max(grid_B):.1f} °C", delta=f"{temp_diff:.1f} °C (방열 효과)")

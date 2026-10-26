# pages/1_Single_Hotspot.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

def apply_space_theme():
    # 웅장한 우주 배경 및 Glassmorphism UI 적용을 위한 CSS 주입 함수
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
apply_space_theme()

st.title("1️⃣ 단일 핫스팟 3D 열 확산 시뮬레이션")

# [핵심 로직] 유한차분법(FDM) 기반 열 확산 시뮬레이션 물리 엔진
def calculate_heat_diffuse(grid, alpha, time_steps, hotspots, hotspot_temp):
    try:
        # 배열 복사 (원본 초기 상태 보존 및 업데이트용 배열 생성)
        new_grid = grid.copy()
        
        # 지정된 시간 흐름(time_steps)만큼 열 방정식 연산 반복 수행
        for step in range(time_steps):
            # 행렬 슬라이싱을 이용해 상, 하, 좌, 우 이웃 노드의 온도 데이터 추출
            up = grid[:-2, 1:-1]; down = grid[2:, 1:-1]
            left = grid[1:-1, :-2]; right = grid[1:-1, 2:]
            center = grid[1:-1, 1:-1]
            
            # 유한차분법(FDM) 수식을 적용하여 현재 노드의 다음 스텝 온도 계산
            new_grid[1:-1, 1:-1] = center + alpha * (up + down + left + right - 4 * center)
            grid = new_grid.copy() # 상태 업데이트
            
            # 디리클레 경계 조건(Dirichlet Boundary Condition) 적용: 
            # 트랜지스터가 켜져있는 동안 핫스팟 좌표는 항상 초기 발열 온도를 지속적으로 유지함
            for (x, y) in hotspots:
                grid[y, x] = hotspot_temp
                
        return grid
    # 수치해석 과정 중 발산(오버플로우) 등 에러 발생 시 예외 처리
    except Exception as e:
        st.error(f"시뮬레이션 연산 오류: {e}")
        return grid

# [시각화 로직] 2D 배열 데이터를 3D Surface 그래프로 렌더링
def plot_3d_surface(grid, title_text):
    fig = go.Figure(data=[go.Surface(z=grid, colorscale='Inferno')])
    # Z축 범위(25~120도)를 고정하여 여러 모델 간의 직관적인 높이 비교를 가능하게 함
    fig.update_layout(title=title_text, scene=dict(zaxis=dict(range=[25, 120])), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

# UI 변수 설정 (사용자가 조작할 수 있는 조작 변인)
st.sidebar.header("⚙️ 시뮬레이션 설정")
grid_size = st.sidebar.slider("격자 크기", 20, 100, 40)
hotspot_temp = st.sidebar.slider("핫스팟 초기 온도", 50, 150, 100)
alpha = st.sidebar.slider("열전도율 (Alpha)", 0.01, 0.20, 0.10)
time_steps = st.sidebar.slider("시간 흐름 (Steps)", 1, 500, 200)

if st.button("▶️ 3D 시뮬레이션 시작"):
    with st.spinner('계산 중...'):
        # 상온(25도)을 기본 베이스 온도로 하는 초기 칩 격자 생성
        initial_grid = np.ones((grid_size, grid_size)) * 25.0
        center = grid_size // 2
        hotspots = [(center, center)] # 칩의 정중앙 좌표 설정
        
        final_grid = calculate_heat_diffuse(initial_grid, alpha, time_steps, hotspots, hotspot_temp)
        st.plotly_chart(plot_3d_surface(final_grid, "Single Hotspot (3D)"), use_container_width=True)

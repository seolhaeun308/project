# pages/4_Quantum_Tunneling.py
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

st.set_page_config(page_title="4. 양자 터널링 시뮬레이션", layout="wide")
apply_space_theme()

st.title("4️⃣ 열-양자 다중물리: 산소 공공 및 터널링 시뮬레이션")
st.write("열 확산으로 인해 산화물 반도체 내부의 **산소 공공(Oxygen Vacancy)**이 어떻게 이동하며, 이것이 전자의 **양자 터널링(Quantum Tunneling)** 확률에 어떤 영향을 미치는지 WKB 근사법을 통해 시뮬레이션합니다.")

# 1. 물리 엔진: 열 확산 계산 (FDM)
def calculate_heat_diffuse(size, time_steps, temp):
    grid = np.ones((size, size)) * 25.0
    center = size // 2
    alpha = 0.10
    for step in range(time_steps):
        new_grid = grid.copy()
        new_grid[1:-1, 1:-1] = grid[1:-1, 1:-1] + alpha * (grid[:-2, 1:-1] + grid[2:, 1:-1] + grid[1:-1, :-2] + grid[1:-1, 2:] - 4 * grid[1:-1, 1:-1])
        grid = new_grid.copy()
        grid[center, center] = temp
    return grid

# 2. 물리 엔진: 산소 공공 밀도 계산 (아레니우스 방정식 기반)
def calculate_oxygen_vacancy(temp_grid, activation_energy):
    k_B = 8.617e-5  # 볼츠만 상수 (eV/K)
    temp_kelvin = temp_grid + 273.15
    # 온도가 높을수록 결함 생성 확률 기하급수적 증가 (Arrhenius Equation)
    vacancy_density = np.exp(-activation_energy / (k_B * temp_kelvin))
    # 시각화를 위한 정규화 및 스케일링
    vacancy_density = (vacancy_density / np.max(vacancy_density)) * 100 
    return vacancy_density

# 3. 물리 엔진: 양자 터널링 확률 계산 (WKB 근사법 기반)
def calculate_tunneling_prob(max_vacancy, barrier_height):
    # 공공 밀도가 높을수록 전자 이동 거리(d)가 짧아짐을 가정한 모델링
    distance_d = 10.0 / (max_vacancy ** 0.5 + 0.1) 
    # WKB Approximation 간소화 모델: P ~ exp(-d * sqrt(V))
    probability = np.exp(-0.5 * distance_d * np.sqrt(barrier_height)) * 100 
    return probability

def plot_3d_surface(grid, title_text, color_theme, z_range):
    fig = go.Figure(data=[go.Surface(z=grid, colorscale=color_theme)])
    fig.update_layout(title=title_text, scene=dict(zaxis=dict(range=z_range)), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, b=0, t=40))
    return fig

# UI 설정
st.sidebar.header("⚙️ 양자역학 변수 설정")
grid_size = st.sidebar.slider("격자 크기", 20, 80, 40)
hotspot_temp = st.sidebar.slider("핫스팟 발열 온도 (°C)", 50, 200, 120)
activation_energy = st.sidebar.slider("산소 공공 활성화 에너지 (eV)", 0.1, 1.0, 0.5, step=0.1)
barrier_height = st.sidebar.slider("양자 에너지 장벽 (eV)", 1.0, 5.0, 2.0, step=0.1)
time_steps = 300 

if st.button("🌌 다중물리(열-양자) 시뮬레이션 시작"):
    with st.spinner('아레니우스 방정식 및 WKB 근사법 계산 중...'):
        # 계산 수행
        temp_grid = calculate_heat_diffuse(grid_size, time_steps, hotspot_temp)
        vacancy_grid = calculate_oxygen_vacancy(temp_grid, activation_energy)
        
        max_vacancy = np.max(vacancy_grid)
        tunneling_prob = calculate_tunneling_prob(max_vacancy, barrier_height)

        # 결과 출력
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🔥 1단계: 반도체 열 분포도")
            st.plotly_chart(plot_3d_surface(temp_grid, "Temperature Map (°C)", 'Inferno', [25, 200]), use_container_width=True)
            st.metric(label="최고 온도", value=f"{np.max(temp_grid):.1f} °C")
            
        with col2:
            st.markdown("### ⚛️ 2단계: 산소 공공(Defect) 밀도")
            st.plotly_chart(plot_3d_surface(vacancy_grid, "Oxygen Vacancy Density (a.u.)", 'Viridis', [0, 100]), use_container_width=True)
            st.metric(label="전자의 양자 터널링 확률", value=f"{tunneling_prob:.6f} %", delta="WKB 근사법 적용")
            
        st.success(f"💡 **물리학적 결론:** 국소적인 열(온도) 상승이 산소 공공의 배열을 변화시키며, 촘촘해진 공공 사이로 전자가 에너지 장벽을 뚫고 지나가는 **양자 터널링(Trap-Assisted Tunneling) 확률이 {tunneling_prob:.6f}% 로 도출**되었습니다. 이는 차세대 뉴로모픽 멤리스터 소자 설계의 핵심 원리입니다.")

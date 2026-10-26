# pages/4_Quantum_Tunneling.py
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

st.set_page_config(page_title="4. 열-양자 다중물리 애니메이션", layout="wide")
apply_space_theme()

st.title("4️⃣ 열-양자 다중물리: 산소 공공 및 터널링 애니메이션")
st.write("열이 확산됨에 따라 산소 공공(Defect)이 집중되고, 전자의 양자 터널링 확률이 시시각각 변화하는 과정을 애니메이션으로 시각화합니다.")

@st.cache_data
def run_quantum_simulation(size, total_steps, temp, activation_energy, barrier_height):
    grid = np.ones((size, size)) * 25.0
    center = size // 2
    alpha = 0.10
    
    k_B = 8.617e-5
    history_data = []
    
    current_grid = grid.copy()
    for step in range(total_steps):
        new_grid = current_grid.copy()
        new_grid[1:-1, 1:-1] = current_grid[1:-1, 1:-1] + alpha * (current_grid[:-2, 1:-1] + current_grid[2:, 1:-1] + current_grid[1:-1, :-2] + current_grid[1:-1, 2:] - 4 * current_grid[1:-1, 1:-1])
        current_grid = new_grid.copy()
        current_grid[center, center] = temp
        
        # 아레니우스 방정식 적용 산소 공공 계산
        temp_kelvin = current_grid + 273.15
        vacancy_density = np.exp(-activation_energy / (k_B * temp_kelvin))
        vacancy_density = (vacancy_density / np.max(vacancy_density)) * 100
        
        # WKB 근사법 터널링 확률 계산
        max_v = np.max(vacancy_density)
        distance_d = 10.0 / (max_v ** 0.5 + 0.1)
        prob = np.exp(-0.5 * distance_d * np.sqrt(barrier_height)) * 100
        
        history_data.append((current_grid.copy(), vacancy_density.copy(), prob))
        
    return history_data

def plot_3d_surface(grid, title_text, color_theme, z_range):
    fig = go.Figure(data=[go.Surface(z=grid, colorscale=color_theme)])
    fig.update_layout(title=title_text, scene=dict(zaxis=dict(range=z_range)), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, b=0, t=40))
    return fig

st.sidebar.header("⚙️ 다중물리 변수 설정")
grid_size = st.sidebar.slider("격자 크기", 20, 60, 40)
hotspot_temp = st.sidebar.slider("핫스팟 발열 온도 (°C)", 50, 200, 120)
activation_energy = st.sidebar.slider("산소 공공 활성화 에너지 (eV)", 0.1, 1.0, 0.5, step=0.1)
barrier_height = st.sidebar.slider("양자 에너지 장벽 (eV)", 1.0, 5.0, 2.0, step=0.1)
total_steps = 100

if st.button("🌌 다중물리 애니메이션 재생"):
    history = run_quantum_simulation(grid_size, total_steps, hotspot_temp, activation_energy, barrier_height)
    
    col1, col2 = st.columns(2)
    p1 = col1.empty()
    p2 = col2.empty()
    metric_placeholder = st.empty()
    progress_bar = st.progress(0)
    
    for i, (t_grid, v_grid, prob) in enumerate(history):
        fig1 = plot_3d_surface(t_grid, f"Temperature Map (Step {i+1})", 'Inferno', [25, 200])
        fig2 = plot_3d_surface(v_grid, f"Oxygen Vacancy Density (Step {i+1})", 'Viridis', [0, 100])
        
        p1.plotly_chart(fig1, use_container_width=True)
        p2.plotly_chart(fig2, use_container_width=True)
        metric_placeholder.metric(label="현재 전자의 양자 터널링 확률 (WKB 모델)", value=f"{prob:.6f} %")
        
        progress_bar.progress((i + 1) / total_steps)
        time.sleep(0.03)
        
    st.success("⚛️ 다중물리 시뮬레이션 애니메이션 재생 완료!")

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

st.set_page_config(page_title="3. TSV 최적화", layout="wide")
apply_space_theme()

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
    fig.update_layout(title=title_text, scene=dict(zaxis=dict(range=[25, 120])), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, b=0, t=40))
    return fig

grid_size = st.sidebar.slider("격자 크기", 20, 100, 40)
tsv_alpha = st.sidebar.slider("TSV 열전도율 (Copper)", 0.15, 0.25, 0.24)

if st.button("⚖️ 일반 실리콘 vs TSV 칩 비교"):
    center = grid_size // 2; offset = 2
    hotspots = [(center, center)]
    init_grid = np.ones((grid_size, grid_size)) * 25.0
    
    alpha_map_A = np.ones((grid_size, grid_size)) * 0.10
    grid_A = calculate_heat_diffuse(init_grid.copy(), alpha_map_A, 200, hotspots, 100)
    
    alpha_map_B = np.ones((grid_size, grid_size)) * 0.10
    for x, y in [(center-offset, center), (center+offset, center), (center, center-offset), (center, center+offset)]:
        alpha_map_B[y, x] = tsv_alpha 
        
    grid_B = calculate_heat_diffuse(init_grid.copy(), alpha_map_B, 200, hotspots, 100)

    # 💡 UI 레이아웃 최적화 및 에러 없는 정상 렌더링
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_3d_surface(grid_A, "Standard Silicon"), use_container_width=True)
        st.metric(label="일반 실리콘 최고 온도", value=f"{np.max(grid_A):.1f} °C") 
    with col2:
        st.plotly_chart(plot_3d_surface(grid_B, "Silicon with Cu TSV"), use_container_width=True)
        delta_val = np.max(grid_B) - np.max(grid_A)
        # delta_color="inverse"를 통해 온도가 내려갔을 때 초록색 화살표가 뜨도록 설정
        st.metric(label="TSV 적용 최고 온도", value=f"{np.max(grid_B):.1f} °C", delta=f"{delta_val:.1f} °C (TSV 쿨링 효과)", delta_color="inverse")

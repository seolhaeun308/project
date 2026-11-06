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

st.set_page_config(page_title="3. TSV 최적화", layout="wide")
apply_space_theme()

st.title("3️⃣ 이종 소재(TSV 방열 기둥) 적용 시뮬레이션")

def calculate_heat_diffuse(grid, alpha_map, time_steps, hotspots, hotspot_val):
    new_grid = grid.copy()
    inner_alpha = alpha_map[1:-1, 1:-1]
    
    # 발열 에너지는 두 칩 모두 동일하게 공급
    total_heat_power = (hotspot_val - 25.0) * 0.15
    power_per_spot = total_heat_power / len(hotspots)
    
    for step in range(time_steps):
        # 💡 구리 기둥(TSV)이 있는 곳은 inner_alpha 값이 높아 중앙의 열을 주변으로 매우 빠르게 빼앗음
        new_grid[1:-1, 1:-1] = grid[1:-1, 1:-1] + inner_alpha * (grid[:-2, 1:-1] + grid[2:, 1:-1] + grid[1:-1, :-2] + grid[1:-1, 2:] - 4 * grid[1:-1, 1:-1])
        grid = new_grid.copy()
        
        for (x, y) in hotspots:
            grid[y, x] += power_per_spot
            
    return grid

def plot_3d_surface(grid, title_text):
    fig = go.Figure(data=[go.Surface(z=grid, colorscale='Inferno')])
    fig.update_layout(title=title_text, scene=dict(zaxis=dict(range=[25, 180])), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, b=0, t=40))
    return fig

grid_size = st.sidebar.slider("격자 크기", 20, 100, 40)
hotspot_val = st.sidebar.slider("발열 강도 (기준값)", 50, 150, 100)
tsv_alpha = st.sidebar.slider("TSV 열전도율 (Copper)", 0.15, 0.25, 0.24)

if st.button("⚖️ 일반 실리콘 vs TSV 칩 비교"):
    center = grid_size // 2; offset = 2
    hotspots = [(center, center)]
    init_grid = np.ones((grid_size, grid_size)) * 25.0
    
    alpha_map_A = np.ones((grid_size, grid_size)) * 0.10
    grid_A = calculate_heat_diffuse(init_grid.copy(), alpha_map_A, 200, hotspots, hotspot_val)
    
    alpha_map_B = np.ones((grid_size, grid_size)) * 0.10
    for x, y in [(center-offset, center), (center+offset, center), (center, center-offset), (center, center+offset)]:
        alpha_map_B[y, x] = tsv_alpha 
        
    grid_B = calculate_heat_diffuse(init_grid.copy(), alpha_map_B, 200, hotspots, hotspot_val)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_3d_surface(grid_A, "Standard Silicon"), use_container_width=True)
        st.metric(label="일반 실리콘 최고 온도", value=f"{np.max(grid_A):.1f} °C") 
    with col2:
        st.plotly_chart(plot_3d_surface(grid_B, "Silicon with Cu TSV"), use_container_width=True)
        
        # 💡 구리 기둥이 중앙의 열을 흡수하여 빠르게 흩뿌렸으므로, 모델 B의 최고 온도가 무조건 떨어짐!
        delta_val = np.max(grid_B) - np.max(grid_A)
        st.metric(label="TSV 적용 최고 온도", value=f"{np.max(grid_B):.1f} °C", delta=f"{delta_val:.1f} °C (TSV 쿨링 효과)", delta_color="inverse")

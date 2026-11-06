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
st.write("💡 구리 기둥(TSV)이 Z축(수직)으로 열을 강제 배출하는 **3차원 히트싱크(Heat Sink) 효과**를 물리 엔진에 적용했습니다.")

# [핵심 로직] Z축 수직 방열 효과가 추가된 물리 엔진
def calculate_heat_diffuse(grid, alpha, time_steps, hotspots, hotspot_val, tsv_coords=[], tsv_cooling_rate=0.0):
    new_grid = grid.copy()
    
    # 핫스팟에 공급할 열 에너지
    total_heat_power = (hotspot_val - 25.0) * 0.15
    power_per_spot = total_heat_power / len(hotspots)
    
    for step in range(time_steps):
        # 1. 2D 평면(X, Y축) 열 확산 연산
        laplacian = (grid[:-2, 1:-1] + grid[2:, 1:-1] + grid[1:-1, :-2] + grid[1:-1, 2:] - 4 * grid[1:-1, 1:-1])
        new_grid[1:-1, 1:-1] = grid[1:-1, 1:-1] + alpha * laplacian
        
        grid = new_grid.copy()
        
        # 2. 💡 TSV 구리 기둥의 수직(Z축) 쿨링 효과 (뉴턴의 냉각 법칙 적용)
        for (x, y) in tsv_coords:
            # 주변 온도가 상온(25도)보다 높을 경우, 수직으로 열을 빠르게 흡수해 배출함
            grid[y, x] -= tsv_cooling_rate * (grid[y, x] - 25.0)
            
        # 3. 중앙 핫스팟 열 에너지 지속 공급
        for (x, y) in hotspots:
            grid[y, x] += power_per_spot
            
    return grid

def plot_3d_surface(grid, title_text):
    fig = go.Figure(data=[go.Surface(z=grid, colorscale='Inferno')])
    fig.update_layout(title=title_text, scene=dict(zaxis=dict(range=[25, 180])), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, b=0, t=40))
    return fig

grid_size = st.sidebar.slider("격자 크기", 20, 100, 40)
hotspot_val = st.sidebar.slider("발열 강도 (기준값)", 50, 150, 100)
# 열전도율 대신 '수직 쿨링 배출 속도'로 변수 변경
tsv_cooling = st.sidebar.slider("TSV 방열 배출 성능 (Cooling Rate)", 0.01, 0.15, 0.08)

if st.button("⚖️ 일반 실리콘 vs TSV 칩 비교"):
    center = grid_size // 2
    hotspots = [(center, center)]
    init_grid = np.ones((grid_size, grid_size)) * 25.0
    
    # 모델 A (대조군): 일반 실리콘 (TSV 없음, 수직 방열 0.0)
    grid_A = calculate_heat_diffuse(init_grid.copy(), 0.10, 200, hotspots, hotspot_val, tsv_coords=[], tsv_cooling_rate=0.0)
    
    # 모델 B (실험군): 구리 TSV 기둥 적용
    offset = 5
    tsv_coords_list = []
    
    # 💡 방열 효과를 시각적으로 뚜렷하게 보기 위해, TSV를 1픽셀이 아닌 3x3 두께의 기둥 4개로 만듦
    for cx, cy in [(center-offset, center), (center+offset, center), (center, center-offset), (center, center+offset)]:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                tsv_coords_list.append((cx+dx, cy+dy))
        
    grid_B = calculate_heat_diffuse(init_grid.copy(), 0.10, 200, hotspots, hotspot_val, tsv_coords=tsv_coords_list, tsv_cooling_rate=tsv_cooling)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_3d_surface(grid_A, "Standard Silicon"), use_container_width=True)
        st.metric(label="일반 실리콘 최고 온도", value=f"{np.max(grid_A):.1f} °C") 
    with col2:
        st.plotly_chart(plot_3d_surface(grid_B, "Silicon with Cu TSV"), use_container_width=True)
        
        # 구리 기둥이 수직으로 열을 강제 배출했으므로 온도가 완벽하게 떨어짐
        delta_val = np.max(grid_B) - np.max(grid_A)
        st.metric(label="TSV 적용 최고 온도", value=f"{np.max(grid_B):.1f} °C", delta=f"{delta_val:.1f} °C (TSV 쿨링 효과)", delta_color="inverse")

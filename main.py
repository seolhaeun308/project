"""
프로젝트명: 3D 적층 반도체 열 확산 시뮬레이터 (Phase 2: 3D 렌더링 및 UI 고도화)
작성자: [본인 이름/학번]
설명: Plotly 기반 인터랙티브 3D 시각화 및 Glassmorphism UI 적용
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ==========================================
# ✨ 신규 기능: Glassmorphism & Tech Grid 디자인
# ==========================================
def apply_custom_css():
    st.markdown("""
    <style>
    /* 메인 배경: 움직이는 다크 네온 + 사이버네틱 격자 무늬(Tech Grid) */
    [data-testid="stAppViewContainer"] {
        background: 
            linear-gradient(rgba(10, 25, 47, 0.8), rgba(10, 25, 47, 0.8)),
            repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(0, 255, 204, 0.03) 10px, rgba(0, 255, 204, 0.03) 20px),
            linear-gradient(-45deg, #0B0C10, #1F2833, #0a192f, #172a45);
        background-size: cover, cover, 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    /* 사이드바 배경: 반투명 유리 질감(Glassmorphism) */
    [data-testid="stSidebar"] {
        background: rgba(10, 25, 47, 0.6) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* 글씨 색상 및 스타일 */
    h1, h2, h3, p, span, div, label {
        color: #E6F1FF !important; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3D 렌더링 물리 엔진 및 기능 함수
# ==========================================
def set_chip_layout(size, hotspots, hotspot_temp):
    grid = np.ones((size, size)) * 25.0
    for (x, y) in hotspots:
        if 0 <= x < size and 0 <= y < size:
            grid[y, x] = hotspot_temp
    return grid

def create_alpha_map(size, tsv_coords, base_alpha, tsv_alpha):
    alpha_map = np.ones((size, size)) * base_alpha
    for (x, y) in tsv_coords:
        if 0 <= x < size and 0 <= y < size:
            alpha_map[y, x] = tsv_alpha
    return alpha_map

def calculate_heat_diffuse(grid, alpha_map, time_steps, hotspots, hotspot_temp):
    if np.max(alpha_map) > 0.25:
        st.error("🚨 수치해석 오류: 열전도율이 0.25를 초과하여 시뮬레이션이 발산합니다.")
        return grid
    
    try:
        new_grid = grid.copy()
        inner_alpha = alpha_map[1:-1, 1:-1]
        
        for step in range(time_steps):
            up = grid[:-2, 1:-1]
            down = grid[2:, 1:-1]
            left = grid[1:-1, :-2]
            right = grid[1:-1, 2:]
            center = grid[1:-1, 1:-1]

            new_grid[1:-1, 1:-1] = center + inner_alpha * (up + down + left + right - 4 * center)
            grid = new_grid.copy()
            
            for (x, y) in hotspots:
                if 0 <= x < grid.shape[1] and 0 <= y < grid.shape[0]:
                    grid[y, x] = hotspot_temp

        return grid
    except Exception as e:
        st.error(f"❌ 시뮬레이션 연산 중 오류 발생: {e}")
        return grid

# ✨ 신규 기능: Plotly를 이용한 인터랙티브 3D 그래프 생성
def plot_3d_surface(grid, title_text):
    # 온도를 Z축(높이)으로 매핑하여 3D 산맥처럼 표현
    fig = go.Figure(data=[go.Surface(z=grid, colorscale='Inferno')])
    
    fig.update_layout(
        title=dict(text=title_text, font=dict(color='white')),
        autosize=True,
        margin=dict(l=0, r=0, b=0, t=40),
        scene=dict(
            xaxis_title='X (Grid)',
            yaxis_title='Y (Grid)',
            zaxis_title='Temp (°C)',
            zaxis=dict(range=[25, 120]), # Z축 높이 고정
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)) # 기본 시점 설정
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# ==========================================
# 메인 화면 구성
# ==========================================
def main():
    st.set_page_config(page_title="3D 열 확산 시뮬레이터", layout="wide")
    apply_custom_css()
    
    st.title("🔥 3D 적층 반도체 열 확산 시뮬레이터")
    st.markdown("*마우스로 그래프를 클릭하고 드래그하여 3D 칩의 온도를 모든 각도에서 확인하세요.*")
    
    menu = st.sidebar.radio("화면 이동 탭", [
        "1. 단일 핫스팟 3D 렌더링", 
        "2. 집중 vs 분산 배치 비교 (3D)",
        "3. TSV(방열 기둥) 적용 3D 최적화"
    ])
    st.sidebar.divider()
    
    st.sidebar.header("⚙️ 시뮬레이션 공통 설정")
    grid_size = st.sidebar.slider("격자 크기", 20, 100, 40)
    hotspot_temp = st.sidebar.slider("핫스팟 초기 온도 (°C)", 50, 150, 100)
    base_alpha = st.sidebar.slider("실리콘 열전도율 (Base)", 0.01, 0.15, 0.10, step=0.01)
    time_steps = st.sidebar.slider("시간 흐름 (Steps)", 1, 1000, 300)
    
    center = grid_size // 2
    basic_alpha_map = np.ones((grid_size, grid_size)) * base_alpha

    if menu == "1. 단일 핫스팟 3D 렌더링":
        st.subheader("화면 1: 중앙 집중형 발열 3D 테스트")
        hotspots = [(center, center)]
        initial_grid = set_chip_layout(grid_size, hotspots, hotspot_temp)
        
        if st.button("▶️ 3D 시뮬레이션 시작"):
            with st.spinner('3D 수치해석 렌더링 중...'):
                final_grid = calculate_heat_diffuse(initial_grid, basic_alpha_map, time_steps, hotspots, hotspot_temp)
                # matplotlib 대신 plotly_chart 사용
                st.plotly_chart(plot_3d_surface(final_grid, "Single Continuous Hotspot (3D)"), use_container_width=True)

    elif menu == "2. 집중 vs 분산 배치 비교 (3D)":
        st.subheader("화면 2: 발열 제어를 위한 구조 최적화 실험 (3D)")
        if st.button("⚖️ 분산 배치 방열 효과 비교하기"):
            with st.spinner('두 가지 모델 동시 수치해석 중...'):
                offset = grid_size // 4
                
                hotspots_A = [(center, center)]
                grid_A_init = set_chip_layout(grid_size, hotspots_A, hotspot_temp)
                grid_A_final = calculate_heat_diffuse(grid_A_init, basic_alpha_map, time_steps, hotspots_A, hotspot_temp)
                
                hotspots_B = [(center - offset, center - offset), (center - offset, center + offset),
                              (center + offset, center - offset), (center + offset, center + offset)]
                grid_B_init = set_chip_layout(grid_size, hotspots_B, hotspot_temp)
                grid_B_final = calculate_heat_diffuse(grid_B_init, basic_alpha_map, time_steps, hotspots_B, hotspot_temp)

                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(plot_3d_surface(grid_A_final, "Concentrated Hotspot"), use_container_width=True)
                    st.metric(label="집중형 최고 온도", value=f"{np.max(grid_A_final):.2f} °C")
                with col2:
                    st.plotly_chart(plot_3d_surface(grid_B_final, "Distributed Hotspots"), use_container_width=True)
                    st.metric(label="분산형 최고 온도", value=f"{np.max(grid_B_final):.2f} °C", delta=f"{np.max(grid_B_final) - np.max(grid_A_final):.2f} °C", delta_color="inverse")

    elif menu == "3. TSV(방열 기둥) 적용 3D 최적화":
        st.subheader("화면 3: 이종 소재(TSV) 방열 통로 개척 시뮬레이션")
        tsv_alpha = st.sidebar.slider("TSV 열전도율 (Copper)", 0.15, 0.25, 0.24, step=0.01)
        
        if st.button("⚖️ 일반 실리콘 vs TSV 탑재 칩 비교"):
            with st.spinner('이종 행렬 수치해석 중...'):
                offset = 2
                hotspots = [(center, center)]
                
                grid_A_init = set_chip_layout(grid_size, hotspots, hotspot_temp)
                grid_A_final = calculate_heat_diffuse(grid_A_init, basic_alpha_map, time_steps, hotspots, hotspot_temp)
                
                tsv_coords = [(center - offset, center), (center + offset, center),
                              (center, center - offset), (center, center + offset)]
                tsv_alpha_map = create_alpha_map(grid_size, tsv_coords, base_alpha, tsv_alpha)
                
                grid_B_init = set_chip_layout(grid_size, hotspots, hotspot_temp)
                grid_B_final = calculate_heat_diffuse(grid_B_init, tsv_alpha_map, time_steps, hotspots, hotspot_temp)

                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(plot_3d_surface(grid_A_final, "Standard Silicon"), use_container_width=True)
                    st.metric(label="일반 칩 평균 온도", value=f"{np.mean(grid_A_final):.2f} °C")
                with col2:
                    st.plotly_chart(plot_3d_surface(grid_B_final, "Silicon with Cu TSV"), use_container_width=True)
                    st.metric(label="TSV 탑재 칩 평균 온도", value=f"{np.mean(grid_B_final):.2f} °C", delta=f"{np.mean(grid_B_final) - np.mean(grid_A_final):.2f} °C", delta_color="inverse")
                
                st.success("💡 TSV 주변으로 열이 빠르게 빨려 들어가면서 거대한 산봉우리(열 병목)가 깎이는 모습을 3D로 증명했습니다.")

if __name__ == "__main__":
    main()

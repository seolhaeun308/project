"""
프로젝트명: 3D 적층 반도체 열 확산 시뮬레이터 (Phase 1: 지속 발열 및 TSV 도입)
작성자: [본인 이름/학번]
설명: 열원이 지속적으로 열을 방출하는 물리 모델 적용 및 TSV 방열 기둥 효과 구현
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def set_chip_layout(size, hotspots, hotspot_temp):
    """기능 1: 반도체 칩 초기 격자 및 복수 핫스팟 생성"""
    grid = np.ones((size, size)) * 25.0
    for (x, y) in hotspots:
        if 0 <= x < size and 0 <= y < size:
            grid[y, x] = hotspot_temp
    return grid

def create_alpha_map(size, tsv_coords, base_alpha, tsv_alpha):
    """기능 4: 이종 소재(Si + Cu TSV) 열전도율 2D 행렬 생성"""
    alpha_map = np.ones((size, size)) * base_alpha
    for (x, y) in tsv_coords:
        if 0 <= x < size and 0 <= y < size:
            alpha_map[y, x] = tsv_alpha
    return alpha_map

def calculate_heat_diffuse(grid, alpha_map, time_steps, hotspots, hotspot_temp):
    """기능 2: 행렬 기반 FDM 열 확산 수치해석 (지속 발열 모델 적용)"""
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
            
            # [핵심 수정] 트랜지스터(핫스팟)가 지속적으로 열을 내도록 온도 고정 (Dirichlet 경계 조건)
            for (x, y) in hotspots:
                if 0 <= x < grid.shape[1] and 0 <= y < grid.shape[0]:
                    grid[y, x] = hotspot_temp

        return grid
    except Exception as e:
        st.error(f"❌ 시뮬레이션 연산 중 오류 발생: {e}")
        return grid

def plot_thermal_heatmap(grid, title_text):
    """기능 3: Matplotlib 온도 히트맵 시각화"""
    fig, ax = plt.subplots(figsize=(5, 4))
    c = ax.imshow(grid, cmap='hot', interpolation='nearest', vmin=25, vmax=100)
    fig.colorbar(c, ax=ax, label="Temp (°C)")
    ax.set_title(title_text)
    return fig

def main():
    st.set_page_config(page_title="열 확산 시뮬레이터", layout="wide")
    st.title("🔥 3D 적층 반도체 열 확산 시뮬레이터")
    
    menu = st.sidebar.radio("화면 이동 탭", [
        "1. 단일 핫스팟 시뮬레이션", 
        "2. 집중 vs 분산 배치 비교",
        "3. TSV(방열 기둥) 적용 최적화"
    ])
    st.sidebar.divider()
    
    st.sidebar.header("⚙️ 시뮬레이션 공통 설정")
    grid_size = st.sidebar.slider("격자 크기", 20, 100, 40)
    hotspot_temp = st.sidebar.slider("핫스팟 초기 온도 (°C)", 50, 150, 100)
    base_alpha = st.sidebar.slider("실리콘 열전도율 (Base)", 0.01, 0.15, 0.10, step=0.01)
    time_steps = st.sidebar.slider("시간 흐름 (Steps)", 1, 1000, 300)
    
    center = grid_size // 2
    basic_alpha_map = np.ones((grid_size, grid_size)) * base_alpha

    # === 화면 1 ===
    if menu == "1. 단일 핫스팟 시뮬레이션":
        st.subheader("화면 1: 중앙 집중형 발열 테스트")
        hotspots = [(center, center)]
        initial_grid = set_chip_layout(grid_size, hotspots, hotspot_temp)
        if st.button("▶️ 시뮬레이션 시작"):
            with st.spinner('계산 중...'):
                final_grid = calculate_heat_diffuse(initial_grid, basic_alpha_map, time_steps, hotspots, hotspot_temp)
                st.pyplot(plot_thermal_heatmap(final_grid, "Single Continuous Hotspot"))

    # === 화면 2 ===
    elif menu == "2. 집중 vs 분산 배치 비교":
        st.subheader("화면 2: 발열 제어를 위한 구조 최적화 실험")
        if st.button("⚖️ 분산 배치 방열 효과 비교하기"):
            with st.spinner('두 가지 모델 동시 수치해석 중...'):
                offset = grid_size // 4
                
                # 모델 A: 중앙 1개
                hotspots_A = [(center, center)]
                grid_A_init = set_chip_layout(grid_size, hotspots_A, hotspot_temp)
                grid_A_final = calculate_heat_diffuse(grid_A_init, basic_alpha_map, time_steps, hotspots_A, hotspot_temp)
                
                # 모델 B: 분산 4개
                hotspots_B = [(center - offset, center - offset), (center - offset, center + offset),
                              (center + offset, center - offset), (center + offset, center + offset)]
                grid_B_init = set_chip_layout(grid_size, hotspots_B, hotspot_temp)
                grid_B_final = calculate_heat_diffuse(grid_B_init, basic_alpha_map, time_steps, hotspots_B, hotspot_temp)

                col1, col2 = st.columns(2)
                with col1:
                    st.pyplot(plot_thermal_heatmap(grid_A_final, "Concentrated Hotspot"))
                    st.metric(label="집중형 최고 온도", value=f"{np.max(grid_A_final):.2f} °C")
                with col2:
                    st.pyplot(plot_thermal_heatmap(grid_B_final, "Distributed Hotspots"))
                    st.metric(label="분산형 최고 온도", value=f"{np.max(grid_B_final):.2f} °C", delta=f"{np.max(grid_B_final) - np.max(grid_A_final):.2f} °C", delta_color="inverse")

    # === 화면 3 ===
    elif menu == "3. TSV(방열 기둥) 적용 최적화":
        st.subheader("화면 3: 이종 소재(TSV) 방열 통로 개척 시뮬레이션")
        tsv_alpha = st.sidebar.slider("TSV 열전도율 (Copper)", 0.15, 0.25, 0.24, step=0.01)
        
        if st.button("⚖️ 일반 실리콘 vs TSV 탑재 칩 비교"):
            with st.spinner('이종 행렬 수치해석 중...'):
                offset = 2
                hotspots = [(center, center)]
                
                # 모델 A: 일반 실리콘
                grid_A_init = set_chip_layout(grid_size, hotspots, hotspot_temp)
                grid_A_final = calculate_heat_diffuse(grid_A_init, basic_alpha_map, time_steps, hotspots, hotspot_temp)
                
                # 모델 B: TSV 기둥 배치
                tsv_coords = [(center - offset, center), (center + offset, center),
                              (center, center - offset), (center, center + offset)]
                tsv_alpha_map = create_alpha_map(grid_size, tsv_coords, base_alpha, tsv_alpha)
                
                grid_B_init = set_chip_layout(grid_size, hotspots, hotspot_temp)
                grid_B_final = calculate_heat_diffuse(grid_B_init, tsv_alpha_map, time_steps, hotspots, hotspot_temp)

                col1, col2 = st.columns(2)
                with col1:
                    st.pyplot(plot_thermal_heatmap(grid_A_final, "Standard Silicon"))
                    st.metric(label="일반 칩 평균 온도", value=f"{np.mean(grid_A_final):.2f} °C")
                with col2:
                    st.pyplot(plot_thermal_heatmap(grid_B_final, "Silicon with Cu TSV"))
                    st.metric(label="TSV 탑재 칩 평균 온도", value=f"{np.mean(grid_B_final):.2f} °C", delta=f"{np.mean(grid_B_final) - np.mean(grid_A_final):.2f} °C", delta_color="inverse")
                
                st.success("💡 TSV 방열 기둥을 통해 열이 더 빠르게 주변으로 퍼져나가며 칩 전체의 열 분포(평균 방열량)가 개선됨을 확인했습니다.")

if __name__ == "__main__":
    main()

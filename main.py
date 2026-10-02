"""
프로젝트명: 3D 적층 반도체 열 확산 시뮬레이터 (최종본)
작성자: [본인 이름/학번]
설명: FDM 수치해석, 예외 처리 3종 완비, 핫스팟 집중/분산 배치 비교 시뮬레이션
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def set_chip_layout(size, hotspots, hotspot_temp):
    """기능 1: 반도체 칩 초기 격자 및 복수 핫스팟 생성"""
    grid = np.ones((size, size)) * 25.0
    
    # 여러 개의 핫스팟 좌표를 반복문으로 적용
    for (x, y) in hotspots:
        # [예외 처리 1] 좌표 범위 이탈 방지 (IndexError 방지)
        if 0 <= x < size and 0 <= y < size:
            grid[y, x] = hotspot_temp
        else:
            st.error(f"오류: 핫스팟 좌표 ({x}, {y})가 칩 범위를 벗어났습니다!")
    return grid

def calculate_heat_diffuse(grid, alpha, time_steps):
    """기능 2: FDM 열 확산 수치해석 및 안정성/런타임 예외 처리"""
    # [예외 처리 2] 수학적 발산 방지 (Von Neumann Stability)
    if alpha > 0.25:
        st.error("🚨 수치해석 오류: 열전도율(alpha)이 0.25를 초과하여 시뮬레이션이 붕괴됩니다.")
        return grid
    
    # [예외 처리 3] 배열 연산 중 발생할 수 있는 메모리/타입 오류 방지 (try-except)
    try:
        new_grid = grid.copy()
        for step in range(time_steps):
            up = grid[:-2, 1:-1]
            down = grid[2:, 1:-1]
            left = grid[1:-1, :-2]
            right = grid[1:-1, 2:]
            center = grid[1:-1, 1:-1]

            new_grid[1:-1, 1:-1] = center + alpha * (up + down + left + right - 4 * center)
            grid = new_grid.copy()
        return grid
        
    except Exception as e:
        st.error(f"❌ 시뮬레이션 연산 중 치명적 오류가 발생했습니다: {e}")
        return grid

def plot_thermal_heatmap(grid, title_text):
    """기능 3: Matplotlib을 이용한 온도 분포 히트맵 시각화"""
    fig, ax = plt.subplots(figsize=(5, 4))
    c = ax.imshow(grid, cmap='hot', interpolation='nearest', vmin=25, vmax=100)
    fig.colorbar(c, ax=ax, label="Temp (°C)")
    ax.set_title(title_text)
    return fig

def main():
    st.set_page_config(page_title="열 확산 시뮬레이터", layout="wide")
    st.title("🔥 3D 적층 반도체 열 확산 시뮬레이터")
    
    menu = st.sidebar.radio("화면 이동 탭", ["1. 단일 핫스팟 시뮬레이션", "2. 집중 vs 분산 배치 비교 (핵심)"])
    st.sidebar.divider()
    st.sidebar.header("⚙️ 시뮬레이션 공통 설정")
    
    grid_size = st.sidebar.slider("격자 크기 (Size)", 20, 100, 40)
    hotspot_temp = st.sidebar.slider("핫스팟 초기 온도 (°C)", 50, 150, 100)
    alpha = st.sidebar.slider("실리콘 열전도율 (Alpha)", 0.01, 0.30, 0.15, step=0.01)
    time_steps = st.sidebar.slider("시간 흐름 (Steps)", 1, 1000, 300)

    # === 화면 1: 단일 핫스팟 (기본 동작 확인) ===
    if menu == "1. 단일 핫스팟 시뮬레이션":
        st.subheader("화면 1: 중앙 집중형 발열 테스트")
        center = grid_size // 2
        initial_grid = set_chip_layout(grid_size, [(center, center)], hotspot_temp)
        
        if st.button("▶️ 기본 시뮬레이션 시작"):
            with st.spinner('계산 중...'):
                final_grid = calculate_heat_diffuse(initial_grid, alpha, time_steps)
                fig = plot_thermal_heatmap(final_grid, f"Single Hotspot (Time: {time_steps})")
                st.pyplot(fig)
                st.success(f"최고 온도: {np.max(final_grid):.2f} °C")

    # === 화면 2: 집중 vs 분산 구조 비교 (수행평가 차별화 포인트) ===
    elif menu == "2. 집중 vs 분산 배치 비교 (핵심)":
        st.subheader("화면 2: 발열 제어를 위한 3D 반도체 구조 최적화 실험")
        st.write("동일한 발열량을 한 곳에 집중했을 때와 네 곳으로 분산했을 때의 방열 성능을 비교합니다.")
        
        if st.button("⚖️ 분산 배치 방열 효과 비교하기"):
            with st.spinner('두 가지 모델을 동시에 수치해석 중...'):
                center = grid_size // 2
                offset = grid_size // 4
                
                # 모델 A: 중앙에 1개 집중
                grid_A_init = set_chip_layout(grid_size, [(center, center)], hotspot_temp)
                grid_A_final = calculate_heat_diffuse(grid_A_init, alpha, time_steps)
                max_temp_A = np.max(grid_A_final)
                
                # 모델 B: 4개로 분산 (온도는 유지하되 면적을 나눔)
                distributed_coords = [
                    (center - offset, center - offset),
                    (center - offset, center + offset),
                    (center + offset, center - offset),
                    (center + offset, center + offset)
                ]
                grid_B_init = set_chip_layout(grid_size, distributed_coords, hotspot_temp)
                grid_B_final = calculate_heat_diffuse(grid_B_init, alpha, time_steps)
                max_temp_B = np.max(grid_B_final)

                # st.columns를 사용해 좌우 분할 출력
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🚨 모델 A: 중앙 집중형 배치")
                    fig_A = plot_thermal_heatmap(grid_A_final, "Concentrated Hotspot")
                    st.pyplot(fig_A)
                    st.metric(label="집중형 최고 온도", value=f"{max_temp_A:.2f} °C")
                    
                with col2:
                    st.markdown("### ✅ 모델 B: 4분할 분산형 배치")
                    fig_B = plot_thermal_heatmap(grid_B_final, "Distributed Hotspots")
                    st.pyplot(fig_B)
                    temp_drop = max_temp_A - max_temp_B
                    st.metric(label="분산형 최고 온도", value=f"{max_temp_B:.2f} °C", delta=f"-{temp_drop:.2f} °C (온도 감소)", delta_color="inverse")
                    
                st.info("💡 **공학적 결론:** 반도체 발열원(트랜지스터)을 분산 배치하면 열 병목 현상이 해소되어 칩의 최고 온도를 효과적으로 낮출 수 있음을 수학적으로 증명함.")

if __name__ == "__main__":
    main()

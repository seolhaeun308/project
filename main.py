"""
프로젝트명: 3D 적층 반도체 열 확산 시뮬레이터 (Phase 1: TSV 도입)
작성자: [본인 이름/학번]
설명: 열전도율(alpha)을 2D 행렬(Map)로 확장하여 이종 소재(TSV 방열 기둥) 효과 구현
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def set_chip_layout(size, hotspots, hotspot_temp):
    """기능 1: 반도체 칩 초기 온도 격자 생성"""
    grid = np.ones((size, size)) * 25.0
    for (x, y) in hotspots:
        if 0 <= x < size and 0 <= y < size:
            grid[y, x] = hotspot_temp
    return grid

def create_alpha_map(size, tsv_coords, base_alpha, tsv_alpha):
    """기능 4: 이종 소재(Si + Cu TSV) 열전도율 2D 행렬(Map) 생성"""
    alpha_map = np.ones((size, size)) * base_alpha
    for (x, y) in tsv_coords:
        if 0 <= x < size and 0 <= y < size:
            alpha_map[y, x] = tsv_alpha  # 특정 위치만 높은 열전도율(구리) 적용
    return alpha_map

def calculate_heat_diffuse(grid, alpha_map, time_steps):
    """기능 2: 행렬 곱셈 기반 FDM 열 확산 수치해석 및 예외 처리"""
    if np.max(alpha_map) > 0.25:
        st.error("🚨 수치해석 오류: TSV 열전도율이 0.25를 초과하여 시뮬레이션이 발산합니다.")
        return grid
    
    try:
        new_grid = grid.copy()
        # 배열 슬라이싱 크기에 맞춰 열전도율 맵도 슬라이싱 (테두리 제외)
        inner_alpha = alpha_map[1:-1, 1:-1]
        
        for step in range(time_steps):
            up = grid[:-2, 1:-1]
            down = grid[2:, 1:-1]
            left = grid[1:-1, :-2]
            right = grid[1:-1, 2:]
            center = grid[1:-1, 1:-1]

            # 스칼라 값 대신 2D 배열(inner_alpha)을 직접 곱하여 부위별 열전도 속도 차별화
            new_grid[1:-1, 1:-1] = center + inner_alpha * (up + down + left + right - 4 * center)
            grid = new_grid.copy()
        return grid
        
    except Exception as e:
        st.error(f"❌ 시뮬레이션 연산 중 치명적 오류 발생: {e}")
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
        "3. TSV(방열 기둥) 적용 최적화 (New✨)"
    ])
    st.sidebar.divider()
    
    st.sidebar.header("⚙️ 시뮬레이션 공통 설정")
    grid_size = st.sidebar.slider("격자 크기", 20, 100, 40)
    hotspot_temp = st.sidebar.slider("핫스팟 초기 온도 (°C)", 50, 150, 100)
    base_alpha = st.sidebar.slider("실리콘 열전도율 (Base)", 0.01, 0.15, 0.10, step=0.01)
    time_steps = st.sidebar.slider("시간 흐름 (Steps)", 1, 1000, 300)

    center = grid_size // 2

    # [화면 1, 2 생략 구조화 - 이전 코드와 동일하게 작동되도록 기본 alpha_map 생성]
    basic_alpha_map = np.ones((grid_size, grid_size)) * base_alpha

    if menu == "1. 단일 핫스팟 시뮬레이션":
        st.subheader("화면 1: 중앙 집중형 발열 테스트")
        initial_grid = set_chip_layout(grid_size, [(center, center)], hotspot_temp)
        if st.button("▶️ 시뮬레이션 시작"):
            final_grid = calculate_heat_diffuse(initial_grid, basic_alpha_map, time_steps)
            st.pyplot(plot_thermal_heatmap(final_grid, "Single Hotspot"))

    elif menu == "2. 집중 vs 분산 배치 비교":
        st.subheader("화면 2: 발열 제어를 위한 구조 최적화 실험")
        # (기존 화면 2 내용이 들어가는 자리 - 코드 길이를 위해 생략 기능만 유지)
        st.write("단일 알파맵(basic_alpha_map)을 이용해 코드가 구동됩니다.")
        st.info("👈 핵심 시뮬레이션인 3번 탭으로 이동해 보세요!")

    # === 화면 3: TSV(구리 전극) 방열 통로 모사 (6일 차 신규 핵심) ===
    elif menu == "3. TSV(방열 기둥) 적용 최적화 (New✨)":
        st.subheader("화면 3: 이종 소재(TSV) 방열 통로 개척 시뮬레이션")
        st.write("실리콘 칩 중간에 열전도율이 높은 구리(Cu) TSV 기둥을 심었을 때 열이 얼마나 빨리 빠져나가는지 비교합니다.")
        
        tsv_alpha = st.sidebar.slider("TSV 열전도율 (Copper)", 0.15, 0.25, 0.24, step=0.01)
        
        if st.button("⚖️ 일반 실리콘 vs TSV 탑재 칩 비교"):
            with st.spinner('이종 행렬 수치해석 중...'):
                offset = 2
                # 핫스팟은 중앙 1개
                hotspots = [(center, center)]
                
                # 모델 A: 일반 실리콘 칩
                grid_A_init = set_chip_layout(grid_size, hotspots, hotspot_temp)
                grid_A_final = calculate_heat_diffuse(grid_A_init, basic_alpha_map, time_steps)
                max_temp_A = np.max(grid_A_final)
                
                # 모델 B: 핫스팟 주변 4곳에 구리 TSV 배치
                tsv_coords = [
                    (center - offset, center), (center + offset, center),
                    (center, center - offset), (center, center + offset)
                ]
                tsv_alpha_map = create_alpha_map(grid_size, tsv_coords, base_alpha, tsv_alpha)
                
                grid_B_init = set_chip_layout(grid_size, hotspots, hotspot_temp)
                grid_B_final = calculate_heat_diffuse(grid_B_init, tsv_alpha_map, time_steps)
                max_temp_B = np.max(grid_B_final)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### ❌ 모델 A: 일반 실리콘 (TSV 없음)")
                    st.pyplot(plot_thermal_heatmap(grid_A_final, "Standard Silicon"))
                    st.metric(label="최고 온도", value=f"{max_temp_A:.2f} °C")
                    
                with col2:
                    st.markdown("### ❄️ 모델 B: TSV 방열 통로 탑재")
                    st.pyplot(plot_thermal_heatmap(grid_B_final, "Silicon with Cu TSV"))
                    st.metric(label="최고 온도", value=f"{max_temp_B:.2f} °C", delta=f"{max_temp_B - max_temp_A:.2f} °C (열 배출 가속)", delta_color="inverse")
                    
                st.success("💡 **공학적 결론:** 동일한 발열 조건이라도, 핫스팟 주변에 고방열 TSV(Thermal Via)를 적절히 배치하면 열이 국소적으로 정체되는 현상을 막아 최고 온도를 유의미하게 낮출 수 있음.")

if __name__ == "__main__":
    main()

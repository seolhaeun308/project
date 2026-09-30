"""
프로젝트명: 3D 적층 반도체 열 확산 시뮬레이터
작성자: [설하은/21112]
설명: 유한차분법(FDM) 기반 열 확산 수치해석 공식 및 폰 노이만 안정성 예외 처리 적용
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def set_chip_layout(size, hotspot_x, hotspot_y, hotspot_temp):
    """기능 1: 반도체 칩 초기 격자 및 핫스팟 생성"""
    grid = np.ones((size, size)) * 25.0
    
    # [예외 처리 1] 핫스팟 좌표가 칩 격자 범위를 벗어나지 않을 때만 적용
    if 0 <= hotspot_x < size and 0 <= hotspot_y < size:
        grid[hotspot_y, hotspot_x] = hotspot_temp
    else:
        st.error("오류: 핫스팟 좌표가 칩 범위를 벗어났습니다!")
    return grid

def calculate_heat_diffuse(grid, alpha, time_steps):
    """기능 2: FDM을 이용한 열 확산 계산 및 안정성 예외 처리"""
    # [예외 처리 2] 물리적 안정성 조건(Von Neumann Stability) 검사
    # dt=1, dx=1을 가정할 때, alpha가 0.25를 넘으면 수치해석이 붕괴(발산)함
    if alpha > 0.25:
        st.error("🚨 수치해석 오류: 열전도율(alpha)이 0.25를 초과하면 시뮬레이션 공식이 붕괴됩니다. 값을 낮춰주세요!")
        return grid # 계산을 중단하고 원본 상태 반환

    new_grid = grid.copy()
    
    # 지정된 시간(time_steps)만큼 열 확산 반복
    for step in range(time_steps):
        # 배열 슬라이싱을 이용해 상하좌우 격자의 온도를 추출
        up = grid[:-2, 1:-1]
        down = grid[2:, 1:-1]
        left = grid[1:-1, :-2]
        right = grid[1:-1, 2:]
        center = grid[1:-1, 1:-1]

        # 2차원 열 확산 방정식(Heat Equation) 유한차분법(FDM) 공식 적용
        new_grid[1:-1, 1:-1] = center + alpha * (up + down + left + right - 4 * center)
        
        # 다음 스텝을 위해 업데이트
        grid = new_grid.copy()
        
    return grid

def plot_thermal_heatmap(grid, title_text):
    """기능 3: Matplotlib을 이용한 온도 분포 시각화 (히트맵)"""
    fig, ax = plt.subplots()
    c = ax.imshow(grid, cmap='hot', interpolation='nearest', vmin=25, vmax=100)
    fig.colorbar(c, ax=ax, label="Temperature (Celsius)")
    ax.set_title(title_text)
    st.pyplot(fig)

def main():
    st.title("🔥 3D 적층 반도체 열 확산 시뮬레이터")
    menu = st.sidebar.radio("화면 이동 탭", ["1. 칩 레이아웃 설계", "2. 시뮬레이션 결과"])
    
    st.sidebar.divider()
    st.sidebar.header("⚙️ 시뮬레이션 설정")
    
    # 사이드바 설정 값
    grid_size = st.sidebar.slider("격자 크기 (Size)", 10, 50, 30)
    hotspot_temp = st.sidebar.slider("핫스팟 초기 온도 (°C)", 50, 150, 100)
    
    # 3일 차 추가 변수: 열전도율과 시간
    # 의도적으로 예외 처리를 보여주기 위해 최댓값을 0.30까지 열어둠 (0.25 넘으면 에러 발생)
    alpha = st.sidebar.slider("실리콘 열전도율 (Alpha)", 0.01, 0.30, 0.10, step=0.01)
    time_steps = st.sidebar.slider("시간 흐름 (Steps)", 1, 500, 100)
    
    center_x = grid_size // 2
    center_y = grid_size // 2

    if menu == "1. 칩 레이아웃 설계":
        st.subheader("화면 1: 초기 레이아웃 및 핫스팟 설정")
        initial_grid = set_chip_layout(grid_size, center_x, center_y, hotspot_temp)
        plot_thermal_heatmap(initial_grid, "Initial Hotspot Layout")

    elif menu == "2. 시뮬레이션 결과":
        st.subheader("화면 2: 열 확산 시뮬레이션 (FDM)")
        initial_grid = set_chip_layout(grid_size, center_x, center_y, hotspot_temp)
        
        # 버튼을 누르면 계산 시작
        if st.button("▶️ 열 확산 시뮬레이션 시작"):
            with st.spinner('수치해석 계산 중...'):
                final_grid = calculate_heat_diffuse(initial_grid, alpha, time_steps)
                plot_thermal_heatmap(final_grid, f"Thermal Diffused (Time: {time_steps}, Alpha: {alpha})")
                
                # 최고 온도 출력
                max_temp = np.max(final_grid)
                st.success(f"시뮬레이션 완료! 칩 내부 최고 온도: {max_temp:.2f} °C")

if __name__ == "__main__":
    main()

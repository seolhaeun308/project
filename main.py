"""
프로젝트명: 3D 적층 반도체 열 확산 시뮬레이터
작성자: [설하은/21112]
설명: 화면 2개 분리 및 초기 핫스팟 격자 생성 구현
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def set_chip_layout(size, hotspot_x, hotspot_y, hotspot_temp):
    """기능 1: 반도체 칩 초기 격자 및 핫스팟 생성"""
    # 1. 칩 전체 온도를 상온(25도)으로 초기화한 2D 배열 생성
    grid = np.ones((size, size)) * 25.0
    
    # 2. [예외 처리] 핫스팟 좌표가 칩 격자 범위를 벗어나지 않을 때만 온도 적용
    if 0 <= hotspot_x < size and 0 <= hotspot_y < size:
        grid[hotspot_y, hotspot_x] = hotspot_temp
    else:
        st.error("오류: 핫스팟 좌표가 칩 범위를 벗어났습니다!")
        
    return grid

def plot_thermal_heatmap(grid, title_text):
    """기능 3: Matplotlib을 이용한 온도 분포 시각화 (히트맵)"""
    fig, ax = plt.subplots()
    # cmap='hot'으로 온도를 색상(검정-빨강-노랑-흰색)으로 표현
    c = ax.imshow(grid, cmap='hot', interpolation='nearest', vmin=25, vmax=100)
    fig.colorbar(c, ax=ax, label="Temperature (Celsius)")
    ax.set_title(title_text)
    
    # 스트림릿 화면에 그래프 띄우기
    st.pyplot(fig)

def main():
    st.title("🔥 3D 적층 반도체 열 확산 시뮬레이터")
    
    # [수행평가 충족] 사이드바를 이용한 '2개 이상의 화면' 구성 및 화면 이동
    menu = st.sidebar.radio("화면 이동 탭", ["1. 칩 레이아웃 설계", "2. 시뮬레이션 결과"])
    
    st.sidebar.divider()
    
    # 사이드바 설정 값
    st.sidebar.header("⚙️ 기본 설정")
    grid_size = st.sidebar.slider("격자 크기 (Size)", 10, 50, 20)
    hotspot_temp = st.sidebar.slider("핫스팟 온도 (°C)", 50, 150, 100)
    
    # === 화면 1: 칩 레이아웃 설계 ===
    if menu == "1. 칩 레이아웃 설계":
        st.subheader("화면 1: 초기 레이아웃 및 핫스팟 설정")
        st.write("반도체 내부의 열원(핫스팟) 위치를 확인하는 화면입니다.")
        
        # 칩의 정중앙에 핫스팟 좌표 설정
        center_x = grid_size // 2
        center_y = grid_size // 2
        
        # 격자 생성 및 시각화 함수 호출
        initial_grid = set_chip_layout(grid_size, center_x, center_y, hotspot_temp)
        plot_thermal_heatmap(initial_grid, "Initial Hotspot Layout")
        
        st.info("👈 왼쪽 사이드바에서 '2. 시뮬레이션 결과'를 클릭해 열 확산을 확인하세요.")

    # === 화면 2: 시뮬레이션 결과 ===
    elif menu == "2. 시뮬레이션 결과":
        st.subheader("화면 2: 열 확산 시뮬레이션 (FDM)")
        st.write("시간이 흐름에 따라 열이 어떻게 퍼져나가는지 수치해석한 결과입니다.")
        st.warning("수치해석 수학 모듈(FDM)은 다음 단계(3일 차)에서 구현됩니다!")

if __name__ == "__main__":
    main()

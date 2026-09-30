"""
프로젝트명: 3D 적층 반도체 열 확산 시뮬레이터
작성자: [본인 이름/학번]
설명: Streamlit을 활용한 유한차분법(FDM) 열 확산 웹 시뮬레이터 뼈대
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def set_chip_layout(size):
    """기능 1: 반도체 칩 레이아웃 설정"""
    # print 대신 st.success를 쓰면 화면에 예쁜 초록색 알림창이 뜹니다.
    st.success(f"[시스템] {size}x{size} 크기의 칩 레이아웃이 설정되었습니다.")
    pass

def calculate_heat_diffuse():
    """기능 2: 열 확산 방정식 계산"""
    st.info("[시스템] 열 확산 수치해석(FDM) 모듈 대기 중... (2~3일 차 구현)")
    pass

def plot_thermal_heatmap():
    """기능 3: 결과 시각화"""
    st.warning("[시스템] 히트맵 시각화 준비 중... (5일 차 구현)")
    pass

def main():
    # 1. 웹 화면 제목과 설명 (st.title, st.write 사용)
    st.title("🔥 3D 적층 반도체 열 확산 시뮬레이터")
    st.write("**작성자:** [설하은/21112]")
    st.write("차세대 반도체의 열 병목 현상(Thermal Bottleneck)을 분석하기 위해, 2차원 열 확산 방정식을 유한차분법(FDM)으로 시뮬레이션하는 프로그램입니다.")
    
    st.divider() # 가로 줄 긋기
    
    # 2. 사이드바(Sidebar)에 설정 메뉴 만들기
    st.sidebar.header("⚙️ 시뮬레이션 설정")
    grid_size = st.sidebar.slider("격자 크기 (Size)", 10, 100, 50)
    
    # 3. 버튼을 누르면 실행되도록 만들기
    if st.button("🚀 시뮬레이션 시작"):
        set_chip_layout(size=grid_size)
        calculate_heat_diffuse()
        plot_thermal_heatmap()

if __name__ == "__main__":
    main()

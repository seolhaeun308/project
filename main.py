"""
프로젝트명: 3D 적층 반도체 열 확산 시뮬레이터
작성자: [본인 이름/학번]
설명: 유한차분법(FDM)을 이용하여 반도체 칩 내부의 열 확산을 시뮬레이션합니다.
"""

import numpy as np
import matplotlib.pyplot as plt

def set_chip_layout(size, hotspot_coords):
    """
    기능 1: 반도체 칩의 초기 레이아웃과 핫스팟(발열원) 위치를 설정합니다.
    - size: 칩의 2D 격자 크기 (예: 50x50)
    - hotspot_coords: 발열이 발생하는 트랜지스터 밀집 구역의 좌표 리스트
    """
    # TODO: 2일 차에 격자 생성(np.zeros) 및 초기 온도 설정 로직 구현 예정
    print("[시스템] 칩 레이아웃이 설정되었습니다.")
    pass

def calculate_heat_diffuse(grid, alpha, time_steps):
    """
    기능 2: 2차원 열 확산 방정식을 수치해석(FDM)으로 계산합니다.
    - grid: 현재 온도 분포 격자
    - alpha: 실리콘 반도체의 열전도율
    - time_steps: 시뮬레이션 반복 횟수
    """
    # TODO: 3일 차에 유한차분법(FDM) 수학 공식 적용 예정
    print("[시스템] 열 확산 계산이 완료되었습니다.")
    pass

def plot_thermal_heatmap(grid):
    """
    기능 3: 계산된 반도체 칩의 온도 분포를 시각화합니다.
    - grid: 최종 온도 분포가 담긴 2D 배열
    """
    # TODO: 5일 차에 Matplotlib 히트맵 출력 기능 구현 예정
    print("[시스템] 히트맵 시각화를 준비합니다.")
    pass

def main():
    """
    메인 실행 함수: 전체 시뮬레이션의 흐름을 제어합니다.
    """
    print("=== 반도체 열 확산 시뮬레이터를 시작합니다 ===")
    
    # 1. 레이아웃 설정
    set_chip_layout(size=50, hotspot_coords=[(25, 25)])
    
    # 2. 열 확산 계산
    calculate_heat_diffuse(grid=[], alpha=0.01, time_steps=100)
    
    # 3. 결과 시각화
    plot_thermal_heatmap(grid=[])

# 스크립트로 직접 실행될 때만 main() 함수 호출
if __name__ == "__main__":
    main()

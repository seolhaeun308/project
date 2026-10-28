# backend_server.py
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

# 전문 계산 서버(요리사) 생성
app = FastAPI()

# 프론트엔드(화면)에서 넘겨줄 재료(데이터) 목록
class Params(BaseModel):
    grid_size: int
    hotspot_temp: float
    activation_energy: float
    barrier_height: float
    total_steps: int

# 주문을 받으면 계산을 시작하는 함수
@app.post("/calculate")
def run_simulation(p: Params):
    # 1. 초기 격자 생성
    grid = np.ones((p.grid_size, p.grid_size)) * 25.0
    center = p.grid_size // 2
    alpha = 0.10
    k_B = 8.617e-5
    
    current_grid = grid.copy()
    
    # 2. 열 확산 계산 (FDM)
    for step in range(p.total_steps):
        new_grid = current_grid.copy()
        new_grid[1:-1, 1:-1] = current_grid[1:-1, 1:-1] + alpha * (
            current_grid[:-2, 1:-1] + current_grid[2:, 1:-1] + 
            current_grid[1:-1, :-2] + current_grid[1:-1, 2:] - 4 * current_grid[1:-1, 1:-1]
        )
        current_grid = new_grid.copy()
        current_grid[center, center] = p.hotspot_temp
        
    # 3. 양자 터널링 확률 계산
    temp_kelvin = current_grid + 273.15
    vacancy_density = np.exp(-p.activation_energy / (k_B * temp_kelvin))
    vacancy_density = (vacancy_density / np.max(vacancy_density)) * 100
    
    max_v = np.max(vacancy_density)
    distance_d = 10.0 / (max_v ** 0.5 + 0.1)
    prob = np.exp(-0.5 * distance_d * np.sqrt(p.barrier_height)) * 100
    
    # 4. 계산 끝! 결과를 화면으로 던져줌
    return {
        "temperature_map": current_grid.tolist(),
        "vacancy_map": vacancy_density.tolist(),
        "probability": prob
    }

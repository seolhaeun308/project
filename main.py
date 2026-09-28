import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 물리적 상수 정의 (SI 단위계 변환용)
# ==========================================
m_e = 9.109e-31      # 전자의 질량 (kg)
hbar = 1.054e-34     # 디랙 상수 (J·s, 플랑크 상수 / 2pi)
eV_to_J = 1.602e-19  # 전자볼트(eV) -> 줄(J) 단위 변환 계수
nm_to_m = 1e-9       # 나노미터(nm) -> 미터(m) 단위 변환 계수

# ==========================================
# 2. 핵심 알고리즘 함수 (함수 분리/모듈화)
# ==========================================
def calculate_tunneling_prob(V0_eV, E_eV, L_nm):
    """
    WKB 근사법을 이용한 직사각형 장벽의 양자 터널링 확률 계산 함수
    """
    # [수행평가 요소: 예외 처리 1, 2] 물리적으로 불가능한 값 차단
    if L_nm <= 0:
        raise ValueError("절연막(장벽)의 두께는 0보다 커야 합니다.")
    if V0_eV <= E_eV:
        raise ValueError("전자의 에너지가 장벽보다 높습니다. (양자 터널링이 아닌 고전적 통과 현상 발생)")

    # 단위를 물리 공식에 맞게 국제표준(SI) 단위로 변환
    V0_J = V0_eV * eV_to_J
    E_J = E_eV * eV_to_J
    L_m = L_nm * nm_to_m

    # WKB 근사법 공식: T = exp(-2 * L * sqrt(2 * m * (V0 - E)) / hbar)
    decay_constant = np.sqrt(2 * m_e * (V0_J - E_J)) / hbar
    probability = np.exp(-2 * L_m * decay_constant)
    
    return probability

def monte_carlo_simulation(prob, num_electrons):
    """
    몬테카를로 시뮬레이션: 난수를 생성하여 장벽을 통과한 전자(누설 전류) 수 계산
    """
    # [수행평가 요소: 예외 처리 3]
    if num_electrons <= 0 or not isinstance(num_electrons, int):
        raise TypeError("시뮬레이션 전자 수는 자연수여야 합니다.")

    # 0~1 사이의 난수를 전자 수만큼 생성
    random_values = np.random.rand(num_electrons)
    # 난수가 터널링 확률(prob)보다 작으면 장벽을 통과(누설)한 것으로 간주
    passed_electrons = np.sum(random_values < prob)
    
    return passed_electrons

# ==========================================
# 3. Streamlit 웹 UI 및 시각화 화면 설계
# ==========================================
st.set_page_config(page_title="양자 터널링 시뮬레이터", layout="wide")

st.title("🔬 반도체 양자 터널링 & 누설 전류 시뮬레이터")
st.markdown("""
순수 양자물리학 현상인 **'양자 터널링(Quantum Tunneling)'**이 초미세 반도체 공정에서 어떻게 **'누설 전류(Leakage Current)'**라는 공학적 난제로 작용하는지 파이썬 모델링을 통해 분석합니다.
""")

# 사이드바: 사용자 입력 컨트롤러
st.sidebar.header("⚙️ 반도체 설계 파라미터")
L_nm = st.sidebar.slider("절연막 두께 (nm)", min_value=0.1, max_value=2.0, value=0.5, step=0.1)
V0_eV = st.sidebar.slider("절연막 에너지 장벽 높이 (eV)", min_value=1.0, max_value=10.0, value=5.0, step=0.5)
E_eV = st.sidebar.slider("전자의 에너지 (eV)", min_value=0.1, max_value=9.9, value=1.0, step=0.1)
num_electrons = st.sidebar.number_input("시뮬레이션 투입 전자 수 (개)", min_value=1000, max_value=1000000, value=100000, step=10000)

# 메인 실행 로직
try:
    # 확률 연산 및 시뮬레이션 실행
    tunneling_prob = calculate_tunneling_prob(V0_eV, E_eV, L_nm)
    passed_count = monte_carlo_simulation(tunneling_prob, num_electrons)
    
    # 1. 결과 요약 출력
    st.subheader("📊 시뮬레이션 결과 (WKB 근사 & 몬테카를로)")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**이론적 양자 터널링 확률:**\n\n {tunneling_prob:.4e} ({tunneling_prob * 100:.6f}%)")
    with col2:
        st.warning(f"**누설된 전자 수 (통과/전체):**\n\n {passed_count} 개 / {num_electrons} 개")

    # 2. 데이터 시각화 (두께 변화에 따른 누설 확률 그래프)
    st.markdown("---")
    st.subheader("📈 절연막 두께에 따른 양자 터널링 확률 변화 (Log Scale)")
    
    # 그래프를 위한 배열 데이터 생성 (0.1nm ~ 2.0nm)
    L_array = np.linspace(0.1, 2.0, 100)
    prob_array = [calculate_tunneling_prob(V0_eV, E_eV, l) for l in L_array]

    # Matplotlib 그리기
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(L_array, prob_array, color='red', linewidth=2, label="Tunneling Probability")
    
    # 현재 설정한 두께 위치에 점 찍기
    ax.scatter([L_nm], [tunneling_prob], color='blue', s=100, zorder=5, label=f"Current Target ({L_nm}nm)")
    
    ax.set_yscale('log') # 값이 기하급수적으로 변하므로 로그 스케일 적용
    ax.set_xlabel("Barrier Width (nm)")
    ax.set_ylabel("Tunneling Probability (Log)")
    ax.legend()
    ax.grid(True, which="both", ls="--", alpha=0.5)
    
    st.pyplot(fig)
    
    st.success("💡 **엔지니어링 인사이트:** 절연막 두께가 얇아질수록 확률(누설 전류)이 기하급수적(지수적)으로 폭증하는 것을 확인할 수 있습니다. 이는 3nm 이하 초미세 공정에서 GAA(Gate-All-Around)와 같은 새로운 3D 트랜지스터 구조가 왜 필수적인지를 수학적으로 증명합니다.")

except ValueError as ve:
    # 사용자 입력 오류 시 (예외 처리)
    st.error(f"🚨 물리적 입력 오류: {ve}")
except TypeError as te:
    st.error(f"🚨 데이터 타입 오류: {te}")
except Exception as e:
    st.error(f"🚨 알 수 없는 시스템 오류가 발생했습니다: {e}")

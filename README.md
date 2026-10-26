# 🔥 3D 적층 반도체 열-양자 다중물리 시뮬레이터
(3D IC Thermal Diffusion & Quantum Tunneling Simulator)

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

## 👨‍🔬 1. 프로젝트 소개 (Project Introduction)
현대 반도체 산업은 미세화 한계를 극복하기 위해 칩을 수직으로 쌓아 올리는 **3차원 적층 기술(3D IC, HBM 등)**을 적극 도입하고 있습니다. 하지만 칩 내부에서 발생하는 열이 밖으로 빠져나가지 못하는 **'열 병목 현상(Thermal Bottleneck)'**은 소자의 수명과 성능을 떨어뜨리는 가장 치명적인 난제입니다.

본 프로젝트는 무거운 상용 TCAD 소프트웨어 없이, **유한차분법(FDM)**과 **3D 렌더링(Plotly)**을 활용하여 반도체 내부의 열 확산을 직관적으로 시각화하고 방열 구조(분산 배치, TSV)를 최적화하는 경량 웹 시뮬레이터입니다. 
더 나아가 최신 신소재/물리학 연구(KAIST 산화물 반도체 연구 등)에서 착안하여, 열 확산이 반도체 내부의 **산소 공공(Oxygen Vacancy)** 이동을 유발하고, 이것이 전자의 **양자 터널링(Quantum Tunneling)** 확률에 미치는 영향까지 분석하는 **열역학-양자역학 다중물리(Multiphysics)** 시뮬레이션으로 확장하여 차세대 뉴로모픽 소자의 작동 원리를 구현했습니다.

---

## ✨ 2. 주요 기능 설명 (Key Features)

본 시뮬레이터는 4개의 독립된 다중 페이지(Multipage) 모듈로 구성되어 있습니다.

*   **1️⃣ 단일 핫스팟 3D 열 확산 시뮬레이션**
    *   반도체 정중앙에 위치한 트랜지스터(열원)의 지속 발열 모사 (Dirichlet 경계 조건 적용).
    *   2D 평면을 넘어선 인터랙티브 3D 산맥(Surface) 그래프 렌더링.
*   **2️⃣ 집중 vs 분산 배치 구조 최적화**
    *   동일한 발열량을 1곳에 집중했을 때와 4곳으로 분산 배치했을 때의 방열 효율 비교.
    *   열 분산에 따른 최고 온도 하락 폭(Delta T) 자동 연산 및 시각적 증명.
*   **3️⃣ 이종 소재(TSV 방열 기둥) 최적화**
    *   단일 실리콘(Si) 칩과 핫스팟 주변에 고열전도율의 구리(Cu) **TSV(실리콘 관통 전극)**를 심은 칩의 방열 성능 비교.
    *   이종 열전도율 2D 행렬(`alpha_map`)을 적용한 쿨링 가속 현상 증명.
*   **4️⃣ 열-양자 다중물리 (산소 공공 & 양자 터널링)**
    *   **통계물리:** 아레니우스 방정식(Arrhenius Equation)을 적용하여 온도 상승에 따른 산소 공공(Defect) 밀도 변화 추적.
    *   **양자역학:** WKB 근사법(WKB Approximation)을 적용하여 산소 공공을 통과하는 전자의 양자 터널링 확률(%) 도출.

---

## 🖥️ 3. 앱 사용법 (Usage Guide)

앱을 실행한 후 웹 브라우저에서 다음과 같이 시뮬레이터를 조작할 수 있습니다.

1.  **메뉴 이동:** 좌측 사이드바(Sidebar)의 라디오 버튼을 클릭하여 1~4번 시뮬레이션 페이지로 이동합니다.
2.  **공학 변수 제어:** 사이드바에 위치한 슬라이더(Slider)를 통해 다음 값들을 실시간으로 조절합니다.
    *   `격자 크기`: 시뮬레이션 칩의 해상도 조절
    *   `핫스팟 초기 온도`: 열원의 발열 강도 조절
    *   `열전도율 (Alpha)`: 실리콘 및 구리의 열 전달 속도 제어
    *   `활성화 에너지 / 에너지 장벽` (4번 탭): 양자 터널링 및 결함 생성 난이도 제어
3.  **시뮬레이션 구동:** 화면 중앙의 **[▶️ 시뮬레이션 시작]** 버튼을 클릭하면 내부 물리 엔진(FDM)이 계산을 시작합니다.
4.  **3D 데이터 분석:** 도출된 3D 그래프는 **마우스 휠(확대/축소)**과 **드래그(회전)**를 통해 자유로운 시점에서 열 병목(Hotspot)의 입체적 형태를 분석할 수 있습니다. 좌우로 배치된 두 모델의 최고 온도 변화 수치(초록색/빨간색 지표)를 확인하여 공학적 결론을 도출합니다.

---

## 🚀 4. 코드 실행 방법 (Installation & Execution)

본 프로젝트는 Python 및 Streamlit을 기반으로 동작합니다. 로컬 환경에서 직접 실행하려면 아래의 단계를 순서대로 터미널에 입력하세요.

**1. 깃허브 저장소 클론 (Clone Repository)**
```bash
git clone [https://github.com/사용자아이디/저장소이름.git](https://github.com/사용자아이디/저장소이름.git)
cd 저장소이름

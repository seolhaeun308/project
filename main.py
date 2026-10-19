# main.py (홈 화면)
import streamlit as st

st.set_page_config(page_title="열 확산 시뮬레이터 홈", layout="wide")

st.title("🔥 3D 적층 반도체 열 확산 시뮬레이터")
st.markdown("---")
st.subheader("👨‍🔬 프로젝트 소개")
st.write("""
이 프로젝트는 차세대 3D 수직 적층 반도체(3D IC)에서 발생하는 **'열 병목 현상(Thermal Bottleneck)'**을 
유한차분법(FDM)과 3D 렌더링(Plotly)을 활용해 시각화하고 최적화하는 시뮬레이터입니다.

👈 **왼쪽 사이드바 메뉴**를 클릭하여 각 시뮬레이션 페이지로 이동하세요.
""")

st.info("""
**[페이지 안내]**
1. **Single Hotspot:** 단일 발열원의 기본 열 확산 3D 렌더링
2. **Layout Comparison:** 발열 집중 배치 vs 분산 배치의 방열 효율 3D 비교
3. **TSV Optimization:** 이종 소재(구리 방열 기둥) 탑재를 통한 쿨링 효과 검증
""")

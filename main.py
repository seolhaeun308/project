# main.py
import streamlit as st

def apply_space_theme():
    st.markdown("""
    <style>
    /* 1. 웅장한 심우주(Deep Space) 그라데이션 배경 */
    [data-testid="stAppViewContainer"] {
        background: 
            radial-gradient(circle at 15% 25%, rgba(60, 20, 80, 0.6) 0%, transparent 40%),
            radial-gradient(circle at 75% 65%, rgba(20, 50, 100, 0.6) 0%, transparent 40%),
            linear-gradient(-45deg, #01010a, #0a0520, #010205);
        background-size: 200% 200%;
        animation: cosmicMove 15s ease infinite;
    }
    
    /* 2. 반짝이는 은하수(Stars) 효과 */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: 
            radial-gradient(1.5px 1.5px at 10% 20%, #ffffff, transparent),
            radial-gradient(2px 2px at 30% 60%, #aaccff, transparent),
            radial-gradient(1px 1px at 70% 40%, #ffffff, transparent),
            radial-gradient(1.5px 1.5px at 80% 90%, #aaccff, transparent),
            radial-gradient(2.5px 2.5px at 40% 10%, #ffffff, transparent),
            radial-gradient(1px 1px at 60% 80%, #ffffff, transparent);
        background-size: 150px 150px;
        opacity: 0.6;
        animation: twinkle 5s infinite alternate;
        pointer-events: none;
        z-index: 0;
    }
    
    /* 3. 사이드바 반투명 우주선 유리 질감 */
    [data-testid="stSidebar"] {
        background: rgba(5, 10, 25, 0.4) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* 4. 텍스트 가독성 (홀로그램 스타일) */
    h1, h2, h3, p, span, div, label, li {
        color: #E6F1FF !important; 
        text-shadow: 0px 0px 4px rgba(255,255,255,0.2);
    }
    
    @keyframes cosmicMove {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    @keyframes twinkle {
        0% {opacity: 0.2;}
        100% {opacity: 0.9;}
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="열 확산 시뮬레이터 홈", layout="wide")
apply_space_theme() # 🌌 웅장한 우주 배경 실행!

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

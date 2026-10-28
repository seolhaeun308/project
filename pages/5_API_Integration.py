# pages/5_API_Integration.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import requests # 통신을 위해 필요한 라이브러리

st.set_page_config(page_title="5. 백엔드 분리 최적화", layout="wide")
st.title("5️⃣ 무거운 계산을 외부 서버로 분리한 최적화 버전")
st.write("화면(프론트엔드)이 직접 계산하지 않고, 외부 계산 전용 서버(FastAPI)로 데이터를 보내 결과를 받아옵니다.")

def plot_3d_surface(grid, title_text, color_theme):
    fig = go.Figure(data=[go.Surface(z=grid, colorscale=color_theme)])
    fig.update_layout(title=title_text, scene=dict(zaxis=dict(range=[25, 200])), margin=dict(l=0, r=0, b=0, t=40))
    return fig

st.sidebar.header("⚙️ 변수 설정")
grid_size = st.sidebar.slider("격자 크기", 20, 60, 40)
hotspot_temp = st.sidebar.slider("핫스팟 온도", 50, 200, 120)
activation_energy = st.sidebar.slider("활성화 에너지", 0.1, 1.0, 0.5)
barrier_height = st.sidebar.slider("에너지 장벽", 1.0, 5.0, 2.0)
total_steps = st.sidebar.slider("시뮬레이션 스텝", 50, 300, 100)

if st.button("🚀 계산 서버로 시뮬레이션 요청하기"):
    with st.spinner("계산 전용 서버에서 연산 중..."):
        # 1. 요리사(백엔드)에게 보낼 주문서 작성
        order_data = {
            "grid_size": grid_size,
            "hotspot_temp": hotspot_temp,
            "activation_energy": activation_energy,
            "barrier_height": barrier_height,
            "total_steps": total_steps
        }
        
        try:
            # 2. 통신으로 주문서 보내기 (요청)
            response = requests.post("http://localhost:8000/calculate", json=order_data)
            
            # 3. 요리사가 계산을 무사히 마쳤다면?
            if response.status_code == 200:
                result = response.json()
                
                # 받아온 결과물을 다시 배열로 만들기
                t_grid = np.array(result["temperature_map"])
                v_grid = np.array(result["vacancy_map"])
                prob = result["probability"]
                
                # 화면에 그리기
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(plot_3d_surface(t_grid, "온도 분포 맵", 'Inferno'), use_container_width=True)
                with col2:
                    st.plotly_chart(plot_3d_surface(v_grid, "산소 공공 밀도", 'Viridis'), use_container_width=True)
                    st.metric(label="양자 터널링 확률", value=f"{prob:.6f} %")
                    
                st.success("✅ 백엔드 서버에서 계산 완료 후 데이터를 성공적으로 받아왔습니다!")
            else:
                st.error("서버 계산 실패!")
        except:
            st.error("🚨 서버에 연결할 수 없습니다. 1번 터미널(FastAPI)이 켜져 있는지 확인하세요.")

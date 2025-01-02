import streamlit as st
from streamlit_chat import message
import requests
 
 # API 키 설정
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


# 세션 상태 초기화 
if 'generated' not in st.session_state:
    st.session_state.generated = []
    
if 'past' not in st.session_state:
    st.session_state.past = []

# API 요청 함수 - 사용자 입력을 API로 전송하고 응답을 받아옴
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# 사용자 입력 폼 생성 - 텍스트 입력 필드와 제출 버튼
with st.form('form', clear_on_submit=True):
    user_input = st.text_input('질문을 입력하세요.', '', key='input')
    submitted = st.form_submit_button('입력')

# 입력 처리 및 응답 생성
if submitted and user_input:
    payload = {"inputs": user_input}
    
    output = query(payload)
    
    # 응답 처리
    if output is not None:
        if isinstance(output, list) and len(output) > 0:
            generated_text = output[0].get('generated_text', '')
            st.session_state.past.append(user_input)
            st.session_state.generated.append(generated_text)
        else:
            st.error("예상치 못한 API 응답 형식입니다.")
            st.write("Received output:", output)

# 대화 이력 표시 - 최신 메시지가 위에 오도록 역순으로 표시
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))


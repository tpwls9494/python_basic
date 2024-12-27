import streamlit as st
from streamlit_chat import message
import requests

# 페이지 설정정
st.set_page_config(
    page_title="Chatbot",
    page_icon="💬"
)
 
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


# 초기 설정
if 'generated' not in st.session_state:
    st.session_state.generated = []
    
if 'past' not in st.session_state:
    st.session_state.past = []

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

with st.form('form', clear_on_submit=True):
    user_input = st.text_input('질문을 입력하세요.', '', key='input')
    submitted = st.form_submit_button('입력')

if submitted and user_input:
    payload = {"inputs": user_input}
    
    output = query(payload)
    
    if output is not None:
        if isinstance(output, list) and len(output) > 0:
            generated_text = output[0].get('generated_text', '')
            st.session_state.past.append(user_input)
            st.session_state.generated.append(generated_text)
        else:
            st.error("예상치 못한 API 응답 형식입니다.")
            st.write("Received output:", output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))


if st.button("홈으로 돌아가기 🏠", use_container_width=True):
    st.switch_page("Home.py")
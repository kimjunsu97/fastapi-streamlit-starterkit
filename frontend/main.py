import streamlit as st
from time import sleep

from modules.settings.style import style_global
from modules.settings.page import set_page_config_sidebar_collapsed
from modules.settings.page import make_sidebar

#var
if "auth_status" not in st.session_state:
    st.session_state["auth_status"] = None
if "token_status" not in st.session_state:
    st.session_state["token_status"] = None

#settings
#page
set_page_config_sidebar_collapsed()
#style
style_global()
#sidebar
make_sidebar()



st.markdown(" ")
st.markdown("<h3 style='text-align: center;'>Log in to Dashboard</h3>", unsafe_allow_html=True)
login_info_placeholder = st.container()
with st.form("login_form"):
    st.markdown(" ")
    email = st.text_input("이메일 (Email address)", placeholder="Email")
    email_valid_placeholder = st.container()
    st.markdown(" ")
    password = st.text_input("비밀번호 (Password)", placeholder="Password", type="password")
    password_valid_placeholder = st.container()
    st.markdown(" ")
    submitted = st.form_submit_button("로그인", type="primary", use_container_width=True)
    if submitted:

        #form validate
        from modules.validation.form_validation import (
            validate_email, validate_password)
        valid = False
        if validate_email(email):
            if validate_password(password):
                    valid=True
            else:
                password_valid_placeholder.markdown(":red[비밀번호를 입력하세요 (4자리 이상 확인)]")
        else:
            email_valid_placeholder.markdown(":red[이메일을 입력하세요 (이메일 형식 확인)]")


        if valid==True:
            from modules.auth.api_auth import get_access_token
            data = get_access_token(email=email, password=password)
            
            if data["access_token"]:
                st.session_state["auth_status"] = True
                st.session_state["token_status"] = True
                st.session_state["access_token"] = data["access_token"]
                st.session_state["token_type"] = data["token_type"]
                login_info_placeholder.info("로그인 성공 ! 홈페이지로 이동합니다")
                #show_pages_auth_true()
                #sleep(0.5)
                st.switch_page("pages/hello.py")
            else:
                login_info_placeholder.error("가입한 이메일 아이디와 비밀번호를 확인하세요")
                st.session_state["auth_status"] = False

if st.button("회원가입", use_container_width=True):
    st.switch_page("pages/signup.py")











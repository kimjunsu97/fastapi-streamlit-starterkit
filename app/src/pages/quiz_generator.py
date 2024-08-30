import streamlit as st
import time
from modules.settings.page import set_page_config, make_sidebar
from modules.settings.style import style_global
from modules.auth.api_auth import validate_token, get_user_info
from modules.security.encryption import str_to_asterisk
from modules.validation.key_validation import validate_openai_api_key
from modules.validation.form_validation import validate_text
from modules.quiz.api_quiz import get_batch_quiz, get_stream_quiz, translate_batch_quiz,translate_stream_quiz
from modules.quiz.streamlit_quiz import batch_generation_interface, stream_generation_interface, batch_translation_interface, stream_translation_interface, open_openaiapikey_modal, open_settings_modal
#var
if "auth_status" not in st.session_state:
    st.session_state["auth_status"] = None
if "token_status" not in st.session_state:
    st.session_state["token_status"] = None
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None
if "key_status" not in st.session_state:
    st.session_state["key_status"] = None
if st.session_state["auth_status"]==True:
    st.session_state["user_info"] = get_user_info(token_type=st.session_state["token_type"], access_token=st.session_state["access_token"])
if "quiz_ready" not in st.session_state:
    st.session_state["quiz_ready"] = False
if "translate_ready" not in st.session_state:
    st.session_state["translate_ready"] = False 
if "language" not in st.session_state:
    st.session_state["language"] = None   
if "rerun" not in st.session_state:
    st.session_state["rerun"] = False
if "stream" not in st.session_state:
    st.session_state["stream"] = False

#redirect
if not st.session_state["auth_status"]==True:
    st.session_state = {}
    st.switch_page("main.py")
st.session_state["token_status"] = validate_token(token_type=st.session_state["token_type"], access_token=st.session_state["access_token"])["status"]
if not st.session_state["token_status"]==True:
    st.session_state = {}
    st.switch_page("main.py")

#settings
#page
set_page_config(auth_status=st.session_state["auth_status"],
                layout="wide")
#sidebar
make_sidebar(st.session_state["auth_status"], st.session_state["user_info"])
#style
style_global()
##############################################################################
#custom style
with open('/app/src/modules/quiz/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

# #modal
# @st.dialog(" ", width="small")
# def open_openaiapikey_modal(old_key=None):
#     if old_key:
#         value = old_key
#     else:
#         value = None
#     openai_api_key = st.text_input("OpenAI API KEY", value=value, key="chatbot_api_key", type="password")
#     "[OpenAI API key 알아보기] (https://platform.openai.com/account/api-keys)"
#     key_message_placeholder = st.container()
#     st.markdown(" ")
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("적용", type="primary", use_container_width=True, key="modal_openaiapikey_button"):
#             if validate_openai_api_key(openai_api_key):
#                 st.session_state["key_status"] = True
#                 st.session_state["openai_api_key"] = openai_api_key
#                 st.rerun()
#             else:
#                 key_message_placeholder.error("OpenAI API KEY를 정확히 입력하세요")
#     with col2:
#         if st.button("닫기", type="secondary", use_container_width=True):
#             st.rerun()

# @st.dialog(" ", width="large")
# def open_settings_modal():
#     st.markdown("")
#     with st.form("quiz_generator_form"):
#         st.markdown("퀴즈를 생성할 문서를 입력하세요")
#         document = st.text_area(" ",label_visibility="collapsed")
#         document_valid_placeholder = st.container()
        
#         #quiz content
#         with st.container():
#             st.markdown("퀴즈 콘텐츠를 선택하세요 (1개 이상)")
#             col_1, col_2, col_3, col_4 = st.columns(4)
#             with col_1: 
#                 #Vocabulary Focused Quiz: 단어 중심
#                 tog_content_vocabulary_focused_quiz = st.toggle("단어 중심", value=True)
#             with col_2: 
#                 #Sentence Example Based Quiz: 문장 기반
#                 tog_content_sentence_example_based_quiz = st.toggle("문장 기반", value=True)
#             with col_3:
#                 #Cultural Information Quiz: 문화 정보
#                 tog_content_cultural_information_quiz = st.toggle("문화 정보", value=True)
#             with col_4:
#                 #Word Order Quiz: 단어 순서
#                 tog_content_word_order_quiz = st.toggle("단어 순서", value=True)  
#             tog_content_valid_placeholder = st.container()
#             #quiz type
#             with st.container():
#                 st.markdown("퀴즈 타입을 선택하세요 (1개 이상)")
#                 col_1, col_2, col_3, col_4 = st.columns(4)
#                 with col_1:
#                     #Multiple Choice: 객관식
#                     tog_type_multiple_choice = st.toggle("객관식", value=True)
#                 with col_2:
#                     #True Or False: 참거짓
#                     tog_type_true_or_false = st.toggle("참/거짓", value=True)
#                 with col_3:
#                     #Fill In The Blank: 빈칸채우기
#                     tog_type_fill_in_the_blank = st.toggle("빈칸 채우기", value=True)
#                 with col_4:
#                     st.markdown("")
#                 tog_type_valid_placeholder =  st.container()

#             #quiz number
#             with st.container():
#                 st.markdown("퀴즈 개수를 선택하세요")
#                 number = st.slider(" ", 1, 10, 3,label_visibility="collapsed")

#             submitted = st.form_submit_button("생성 시작", type="primary", use_container_width=True)
#             if submitted:
#                 valid = False
#                 if validate_text(document):
#                     if tog_content_vocabulary_focused_quiz | tog_content_sentence_example_based_quiz | tog_content_cultural_information_quiz | tog_content_word_order_quiz:
#                         if tog_type_multiple_choice | tog_type_true_or_false | tog_type_fill_in_the_blank:
#                             valid = True
#                         else:
#                             tog_type_valid_placeholder.markdown(":red[퀴즈 타입을 1개 이상 선택하세요]")
#                     else:
#                         tog_content_valid_placeholder.markdown(":red[퀴즈 콘텐츠를 1개 이상 선택하세요]")
#                 else:
#                     document_valid_placeholder.markdown(":red[퀴즈를 생성할 문서를 입력하세요 (10자 이상)]")

#                 if valid:
#                     #initialization
#                     st.session_state["quiz"] = {}
#                     st.session_state["quiz"]["input"] = {}
#                     #document
#                     print(document)
#                     st.session_state["quiz"]["input"]["document"] = document
#                     #quiz_content
#                     st.session_state["quiz"]["input"]["quiz_content"] = []
#                     print(tog_content_vocabulary_focused_quiz)
#                     if tog_content_vocabulary_focused_quiz:
#                         st.session_state["quiz"]["input"]["quiz_content"].append("vocabulary_focused")
#                     print(tog_content_sentence_example_based_quiz)
#                     if tog_content_sentence_example_based_quiz:
#                         st.session_state["quiz"]["input"]["quiz_content"].append("sentence_example")
#                     print(tog_content_cultural_information_quiz)
#                     if tog_content_cultural_information_quiz:
#                         st.session_state["quiz"]["input"]["quiz_content"].append("cultural_information")
#                     print(tog_content_word_order_quiz)
#                     if tog_content_word_order_quiz:
#                         st.session_state["quiz"]["input"]["quiz_content"].append("word_order")
#                     #quiz_type
#                     st.session_state["quiz"]["input"]["quiz_type"] = []
#                     print(tog_type_multiple_choice)
#                     if tog_type_multiple_choice:
#                         st.session_state["quiz"]["input"]["quiz_type"].append("multiple_choice")
#                     print(tog_type_true_or_false)
#                     if tog_type_true_or_false:
#                         st.session_state["quiz"]["input"]["quiz_type"].append("true_or_false")
#                     print(tog_type_fill_in_the_blank)
#                     if tog_type_fill_in_the_blank:
#                         st.session_state["quiz"]["input"]["quiz_type"].append("fill_in_the_blank")
#                     print("---")
#                     print(number)
#                     st.session_state["quiz"]["input"]["number"] = number
#                     with st.spinner('퀴즈를 생성 중입니다. 잠시만 기다려 주세요...'):
#                         time.sleep(1)
#                         """
#                         quiz_output = get_quiz(
#                             token_type = st.session_state["token_type"], 
#                             access_token = st.session_state["access_token"],
#                             openai_api_key = st.session_state["openai_api_key"],
#                             document = st.session_state["quiz"]["input"]["document"],
#                             quiz_content = st.session_state["quiz"]["input"]["quiz_content"],
#                             quiz_type = st.session_state["quiz"]["input"]["quiz_type"],
#                             number = st.session_state["quiz"]["input"]["number"]
#                         )
#                         #st.session_state["quiz_messages"].append({"role": "assistant", "content": st.session_state["quiz"]})
#                         st.session_state["quiz_messages"].append({"role": "assistant", "content": quiz_output["results"]})
#                         """
#                         st.session_state["quiz_messages"].append({"role": "assistant", "content": "샘플입니다."})

#                         st.rerun()

#func
def reset_conversation():
  #message 초기화
  st.session_state["quiz_messages"] = [st.session_state["quiz_messages"][0]]
  ##st.session_state.chat_history = None

#main

st.markdown("")

if st.toggle("Activate Streaming", value=st.session_state["stream"]):
    st.session_state["stream"]=True
else:
    st.session_state["stream"] = False
st.write("Stream status:", st.session_state["stream"])

username = st.session_state["user_info"]["username"]
if "quiz_messages" not in st.session_state:
    st.session_state["quiz_messages"] = [{"role": "assistant", "content": f"안녕하세요 {username} 님 !  \n '퀴즈 생성' 버튼을 클릭하여 퀴즈를 생성해 주세요!"}]
if "translated_messages" not in st.session_state:
    st.session_state["translated_messages"] = [{"role": "assistant", "content": f"안녕하세요 {username} 님 !  \n 번역할 내용을 입력해 주세요!"}]

col1, col2 = st.tabs(['Quiz','Translate'])
with col1:
    if st.session_state["rerun"]==True:
        st.session_state["rerun"]=False
        st.rerun()
    if st.session_state['stream']:
        stream_generation_interface()
    else:
        batch_generation_interface()
    but1, but2, but3 = st.columns((1,1,1), gap="small")
    with but1:
        key_placeholder = st.container()
        if not st.session_state["key_status"]==True:
            if key_placeholder.button("OpenAI API KEY", type="primary", use_container_width=True, key="openai_api_key_button"):
                open_openaiapikey_modal()
        else:
            if key_placeholder.button("OpenAI API KEY", type="secondary", use_container_width=True, key="openai_api_key_2_button"):
                open_openaiapikey_modal(old_key=st.session_state["openai_api_key"])
    with but2:
        quiz_gen_placeholder = st.container()
        if not st.session_state["key_status"]==True:
            quiz_gen_placeholder.button("퀴즈 생성", type="primary", disabled=True, use_container_width=True)
        else:
            if quiz_gen_placeholder.button("퀴즈 생성", type="primary", use_container_width=True):
                open_settings_modal()

    with but3:
        quiz_del_placeholder = st.container()
        quiz_del_placeholder.button('대화 삭제', on_click=reset_conversation, use_container_width=True)   

    st.markdown("")

with col2:
    if st.session_state['stream']:
        stream_translation_interface()
    else:
        batch_translation_interface()

##title
# col_1, col_2 = st.columns([1,1])
# with col_1:
#     st.markdown("""<div style="font-size:26px;font-weight:bold;font-family:'Gothic A1';"> 한국어 퀴즈 생성 </div>""", unsafe_allow_html=True)
# with col_2:
#     col_2_1, col_2_2, col_2_3 = st.columns([8,1,1])
#     with col_2_2:
#         if st.button(":material/account_circle:",key="df", use_container_width=False):
#             st.switch_page("pages/my_profile.py")
#     with col_2_3:     
#         if st.button(":material/logout:",key="asdf", use_container_width=False):
#             st.session_state = {}
#             st.switch_page("main.py")
# st.markdown("""<div style="height:0.5px;border:none;color:#D3D3D3;background-color:#D3D3D3;" /> """, unsafe_allow_html=True)
# st.markdown("")
# username = st.session_state["user_info"]["username"]

# col1, col2 = st.columns((3,1), gap="small")

# with col1:
#     with st.container(border=True, height=450):
#         if "quiz_messages" not in st.session_state:
#             st.session_state["quiz_messages"] = [{"role": "assistant", "content": f"안녕하세요 {username} 님 !  \n '퀴즈 생성' 버튼을 클릭하여 퀴즈를 생성해 주세요!"}]
        
#         if st.session_state["quiz_messages"]:

#             #반대 순서로 보기('reversed')
#             for idx, msg in enumerate(st.session_state["quiz_messages"]):
#                 # with st.expander("번역 보기"):
#                 #     trans1, trans2 = st.columns((1,1))
#                 #     with trans1:
#                 #         language = st.selectbox('', ["Vietnamese", "Japanese", "Chinese"], key=f"language_select{idx}",label_visibility="collapsed")
#                 #     with trans2:
#                 #         translate_button =  st.button(f"번역 (메시지)", key=f"translate{idx}", use_container_width=True)
#                 #     if translate_button:
#                 #         with st.spinner('퀴즈를 번역 중입니다. 잠시만 기다려 주세요...'):
#                 #             time.sleep(1)
#                 #             translated_quiz = translate_quiz(
#                 #                 token_type = st.session_state["token_type"], 
#                 #                 access_token = st.session_state["access_token"],
#                 #                 openai_api_key = st.session_state["openai_api_key"],
#                 #                 quiz = msg["content"],
#                 #                 language = language
#                 #             )
#                             # st.session_state["quiz_messages"].append({"role": "assistant", "content": translated_quiz["results"]})
#                             # st.rerun()
#                 #            st.write(translated_quiz["results"])
#                 with st.chat_message(name=msg["role"], avatar="/app/src/images/bot_icon_2.jpg"): #avatar="https://raw.githubusercontent.com/dataprofessor/streamlit-chat-avatar/master/bot-icon.png"
#                     st.markdown(msg["content"])

#     but1, but2, but3 = st.columns((1,1,1), gap="small")
#     with but1:
#         key_placeholder = st.container()
#         if not st.session_state["key_status"]==True:
#             if key_placeholder.button("OpenAI API KEY", type="primary", use_container_width=True, key="openai_api_key_button"):
#                 open_openaiapikey_modal()
#         else:
#             if key_placeholder.button("OpenAI API KEY", type="secondary", use_container_width=True, key="openai_api_key_2_button"):
#                 open_openaiapikey_modal(old_key=st.session_state["openai_api_key"])
#     with but2:
#         quiz_gen_placeholder = st.container()
#         if not st.session_state["key_status"]==True:
#             quiz_gen_placeholder.button("퀴즈 생성", type="primary", disabled=True, use_container_width=True)
#         else:
#             if quiz_gen_placeholder.button("퀴즈 생성", type="primary", use_container_width=True):
#                 open_settings_modal()
#     with but3:
#         quiz_del_placeholder = st.container()
#         quiz_del_placeholder.button('대화 삭제', on_click=reset_conversation, use_container_width=True)
    
#     st.markdown("")

# with col2:
#     # from streamlit_extras.stylable_container import stylable_container
#     # with stylable_container(
#     #     key="quiz_chat",
#     #     css_styles="""{
#     #     border: 1px solid rgba(49, 51, 63, 0.2);
#     #     border-radius: 0.5rem;
#     #     padding: calc(1em - 1px);
#     #     background-color: #F0F2F6;
#     #     button {
#     #             background-color: none;
#     #         }
#     #     }
#     #     """
#     # ):
    
#     with st.container(height=450):
#         with st.popover('번역 언어',use_container_width=True):
#             st.selectbox('From',['English'])
#             language = st.selectbox('To',["Vietnamese", "Japanese", "Chinese"])
#         messages = st.container(height=350)
#     if prompt := st.chat_input("번역할 문장을 입력해 주세요"):
#         messages.chat_message("user").write(prompt)
#         translated_quiz = translate_quiz(
#             token_type = st.session_state["token_type"], 
#             access_token = st.session_state["access_token"],
#             openai_api_key = st.session_state["openai_api_key"],
#             quiz = prompt,
#             language = language)
#         messages.chat_message("assistant").write(translated_quiz["results"])

#     # quiz_tran_placeholder = st.container()
#     # quiz_tran_placeholder.button("대화 번역", use_container_width=True)
#         # key_placeholder = st.container()
#         # quiz_gen_placeholder = st.container()
#         # quiz_tran_placeholder = st.container()
#         # quiz_del_placeholder = st.container()
#         # if not st.session_state["key_status"]==True:
#         #     if key_placeholder.button("OpenAI API KEY", type="primary", use_container_width=True, key="openai_api_key_button"):
#         #         open_openaiapikey_modal()
#         # else:
#         #     if key_placeholder.button("OpenAI API KEY", type="secondary", use_container_width=True, key="openai_api_key_2_button"):
#         #         open_openaiapikey_modal(old_key=st.session_state["openai_api_key"])

#         # if not st.session_state["key_status"]==True:
#         #     quiz_gen_placeholder.button("퀴즈 생성", type="primary", disabled=True, use_container_width=True)
#         # else:
#         #     if quiz_gen_placeholder.button("퀴즈 생성", type="primary", use_container_width=True):
#         #         open_settings_modal()

#         # quiz_tran_placeholder.button("대화 번역", use_container_width=True)

#         # quiz_del_placeholder.button('대화 삭제', on_click=reset_conversation, use_container_width=True)

#         # st.markdown("")
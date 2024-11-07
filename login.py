import json
import streamlit as st
with open('users.json','r') as f:
    users=json.load(f)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
col1, col2, col3 = st.columns(3)
with col2:
    st.image("lf.png")
# st.title("登录系统")
st.markdown(
    "<p style='text-align: center; font-size: 36px; font-weight: bold;'>登录系统</p>",
    unsafe_allow_html=True
)
st.subheader("请输入账户密码")
username=st.text_input("用户名")
password=st.text_input("密码",type="password")
if st.button("登录"):
    if username in users and users[username]==password:
        st.session_state.logged_in=True
        st.write("ok")
        st.rerun()
    else:
        st.session_state.logged_in=False
        st.write("no")

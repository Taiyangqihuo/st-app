import streamlit as st
login_page=st.Page("login.py",title="登录系统")
app_pages=[st.Page("general.py",title="入网信息概览"),st.Page("show2.py",title="用户能耗分析"),st.Page("show3.py",title="用户行为分析")]
if 'logged_in' not in st.session_state or st.session_state.logged_in==False:
    st.session_state.logged_in = False
    pg=st.navigation([login_page])
    pg.run()
else:
    pg=st.navigation(app_pages)
    pg.run()
    if st.sidebar.button("登出"):
        st.session_state.logged_in = False
        st.rerun()



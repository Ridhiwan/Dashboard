import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """ 
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """


def logout():
    if "login" not in st.session_state:
        st.session_state["login"] = False
        switch_page("SignUp or Login")
    else:
        st.session_state["login"] = False
        switch_page("SignUp or Login")

    st.markdown(hide_st_style, unsafe_allow_html=True)


if __name__ == "__main__":
    logout()

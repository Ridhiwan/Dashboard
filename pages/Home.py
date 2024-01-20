import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import base64


# ---- HOME PAGE ----
def homepage():
    # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """ 
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    header {visibility: hidden;}
                    </style>
                    """

    # ---- WELCOME PAGE ----
    buffer, col, buffer2 = st.columns([1, 3, 1])
    with open(r'C:\Users\Zakia\Documents\GitHub\Dashboard\pages\DashyB_logo_cropped.gif', "rb") as gif_file:
        gif_url = base64.b64encode(gif_file.read()).decode("utf-8")
    col.markdown(f'<img src="data:image/gif;base64,{gif_url}" alt="cat gif">', unsafe_allow_html=True, )
    col.markdown("""<h1><strong>Welcome to DashyB!</strong></h1>""", unsafe_allow_html=True)
    col.write("A secure way to analyse your business's data.")

    # ---- PAGE CHANGE ----
    with st.sidebar.container():
        st.header("Type of Analysis")
        analysis = st.radio("Choose one",
                            ["select", "Inventory Analysis", "Sales Analysis", ], )

    if analysis == "Sales Analysis":
        switch_page("Analysis")
    elif analysis == "Inventory Analysis":
        switch_page("Inventory")
    elif analysis == "select":
        pass
    else:
        pass
    st.markdown(hide_st_style, unsafe_allow_html=True)


def home_placeholder(instructions):
    # ---- WELCOME PAGE ----
    buffer, col, buffer2 = st.columns([1, 3, 1])
    with open(r'C:\Users\Zakia\Documents\GitHub\Dashboard\pages\DashyB_logo_cropped.gif', "rb") as gif_file:
        gif_url = base64.b64encode(gif_file.read()).decode("utf-8")
    col.markdown(f'<img src="data:image/gif;base64,{gif_url}" alt="cat gif">', unsafe_allow_html=True, )
    col.markdown("""<h1><strong>Welcome to DashyB!</strong></h1>""", unsafe_allow_html=True)
    col.write(instructions)


if __name__ == "__main__":
    try:
        if st.session_state["login"]:
            homepage()
        else:
            switch_page("SignUp or Login")
    except Exception as e:
        st.error(e)
        switch_page("SignUp or Login")

import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import base64

#---- UPLOAD FILE ----
@st.cache_data(experimental_allow_widgets=True)
def uploaded(key):
    uploaded_file = st.sidebar.file_uploader(label="Upload your file(CSV or Excel)",
        type=['csv','xlsx'],key=key)
    return uploaded_file


#---- HOME PAGE ----
def homepage():
    
    #---- HIDE STREAMLIT STYLE ----
    hide_st_style = """ 
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    header {visibility: hidden;}
                    </style>
                    """
    
    #---- WELCOME PAGE ----
    buffer, col, buffer2 = st.columns([1,3,1])
    with open(r'C:\Users\Zakia\Documents\GitHub\Dashboard\pages\DashyB_logo_cropped.gif', "rb") as gif_file:
        gif_url = base64.b64encode(gif_file.read()).decode("utf-8")
    col.markdown(f'<img src="data:image/gif;base64,{gif_url}" alt="cat gif">', unsafe_allow_html=True,)
    col.markdown("""<h1><strong>Welcome to DashyB!</strong></h1>""", unsafe_allow_html=True)
    col.write("Please upload a CSV or Excel file to analyse.")
    st.markdown(hide_st_style,unsafe_allow_html=True)

if __name__ == "__main__":
    try:
        if st.session_state["login"]:
            file = uploaded("one")
            if file is None:
                homepage()
            elif file is not None:
                switch_page("Analysis")
    except Exception as e:
        st.error(e)
        switch_page("SignUp or Login")
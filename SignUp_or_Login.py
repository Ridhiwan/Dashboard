import pyrebase as pb
import requests
import json
import re
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
st.session_state.update(st.session_state)



st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":bar_chart:",
    layout = "wide",
    )

#---- HIDE STREAMLIT STYLE ----
hide_st_style = """ 
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """


#---- USER AUTHENTICATION ----

# Configuration key
firebaseConfig = {
    'apiKey': "AIzaSyDma6mgidk3SPyShf_TWR8GCiAK93FIgvk",
    'authDomain': "dashboard-cc8d6.firebaseapp.com",
    'projectId': "dashboard-cc8d6",
    'databaseURL': "https://dashboard-cc8d6-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "dashboard-cc8d6.appspot.com",
    'messagingSenderId': "172538484816",
    'appId': "1:172538484816:web:70c21420b0124dc890d955",
    'measurementId': "G-MRJSEC32NG"
  }

# Firebase Authentication
def firebase_auth():
    firebase = pb.initialize_app(firebaseConfig)
    auth = firebase.auth()
    return firebase, auth

# Database
def firebase_db():
    db = firebase.database()
    stg = firebase.storage()
    return db, stg

# Orientation
buffer, col, buffer2 = st.columns([1,3,1])

# Authentication
def sign_up():
    email = col.text_input("Enter your email", placeholder="you@example.com", key="em")
    password = col.text_input("Enter your password", type="password", key="pass")
    confirm_password = col.text_input("Confirm your password", type="password", key="con")
    submit = col.button("Create Account")
    if password != confirm_password:
        submit = False
        col.error("Passwords do not match.")
    elif len(password) < 8:
        submit = False
        col.error("Password must be at least 8 characters long.")
    elif not any(char.isdigit() for char in password):
        submit = False
        col.error("Password must contain at least one digit.")
    elif not any(char.isupper() for char in password):
        submit = False
        col.error("Password must contain at least one uppercase letter.")
    elif not re.search('@dashyb.com', email):
        col.error("You have entered an invalid email")
    else:
        if submit:
            try:     
                auth.create_user_with_email_and_password(email, password)
                col.success('''Your account has been created successfully!
                                Please Login.''')
            except requests.HTTPError as e:
                error_json = e.args[1]
                error = json.loads(error_json)['error']['message']
                col.error(error)
    st.markdown(hide_st_style,unsafe_allow_html=True)

def login():
    email = col.text_input("Enter your email", placeholder="you@example.com")
    password = col.text_input("Enter your password",type="password")
    login = col.button("Login")
    if "login" not in st.session_state:
        st.session_state["login"] = False
    if login:
        try:
            auth.sign_in_with_email_and_password(email, password)
            st.session_state["login"] =True
            switch_page("Home")
        except requests.HTTPError as e:
                    error_json = e.args[1]
                    error = json.loads(error_json)['error']['message']
                    col.error(error)

    st.markdown(hide_st_style,unsafe_allow_html=True)

def logout():
    if "login" not in st.session_state:
        st.session_state["login"] = False
        switch_page("SignUp or Login")
    else:
        st.session_state["login"] = False
        switch_page("SignUp or Login")

    st.markdown(hide_st_style,unsafe_allow_html=True)


if __name__ == '__main__':
    firebase, auth = firebase_auth()
    db, stg = firebase_db()
    select = col.selectbox("Sign up/Login",["Sign up", "Login"],
     help="Click the box to Sign Up or Login")
    if select == "Sign up":
        sign_up()
    if select == "Login":
        login()


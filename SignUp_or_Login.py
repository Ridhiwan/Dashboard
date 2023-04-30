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

# Authentication
def sign_up():
    email = st.text_input("Enter your email", placeholder="you@example.com", key="em")
    password = st.text_input("Enter your password", type="password", key="pass")
    confirm_password = st.text_input("Confirm your password", type="password", key="con")
    submit = st.button("Create Account")
    if password != confirm_password:
        submit = False
        st.error("Passwords do not match.")
    elif len(password) < 8:
        submit = False
        st.error("Password must be at least 8 characters long.")
    elif not any(char.isdigit() for char in password):
        submit = False
        st.error("Password must contain at least one digit.")
    elif not any(char.isupper() for char in password):
        submit = False
        st.error("Password must contain at least one uppercase letter.")
    elif not re.search('@dashy.com', email):
        st.error("You have entered an invalid email")
    elif "signup" not in st.session_state:
        st.session_state["signup"] = False
    else:
        if submit:
            try:     
                account = auth.create_user_with_email_and_password(email, password)
                st.success("Your account has been created successfully!")
                st.session_state["signup"] = True
                switch_page("Analysis")
            except requests.HTTPError as e:
                error_json = e.args[1]
                error = json.loads(error_json)['error']['message']
                st.error(error)
    st.markdown(hide_st_style,unsafe_allow_html=True)

def login():
    email = st.text_input("Enter your email", placeholder="you@example.com")
    password = st.text_input("Enter your password",type="password")
    login = st.button("Login")
    if "login" not in st.session_state:
        st.session_state["login"] = False
    if login:
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state["login"] =True
            switch_page("Analysis")
        except requests.HTTPError as e:
                    error_json = e.args[1]
                    error = json.loads(error_json)['error']['message']
                    st.error(error)

    st.markdown(hide_st_style,unsafe_allow_html=True)


if __name__ == '__main__':
    firebase, auth = firebase_auth()
    db, stg = firebase_db()
    select = st.selectbox("Sign up/Login",["Sign up", "Login"])
    if select == "Sign up":
        sign_up()
    elif select == "Login":
        login()


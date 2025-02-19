import streamlit as st
from services import check_credentials

def login_callback():
    client_id_input = st.session_state.get("client_id_input")
    if check_credentials(client_id_input):
        st.session_state.logged_in = True
        st.session_state.client_id = client_id_input
        st.success("Login successful!")
        st.rerun()  # Refresh the app immediately
    else:
        st.error("Invalid Client ID. Please try again.")

def show_login():
    st.subheader("Login")
    st.text_input("Enter your Client ID (password)", key="client_id_input", type="password")
    st.button("Login", on_click=login_callback)

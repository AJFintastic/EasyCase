# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 12:12:38 2025

@author: user
"""

# login.py

import streamlit as st
from services import check_credentials

def show_login():
    """
    Renders the login section. Prompts the user for a Client ID (used as password).
    """
    st.subheader("Login")

    client_id_input = st.text_input("Enter your Client ID (password)", type="password")
    if st.button("Login"):
        if check_credentials(client_id_input):
            st.session_state.logged_in = True
            st.session_state.client_id = client_id_input
            st.success("Login successful!")
        else:
            st.error("Invalid Client ID. Please try again.")

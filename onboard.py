# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 12:12:49 2025

@author: user
"""

# onboard.py

import streamlit as st
import uuid
from services import clients_data

# Path to the uploaded PDF
MANDATE_FILE_PATH = "AM LAW INC FICA FEE MANDATE 2025.pdf"

def show_onboarding():
    """
    Renders the onboarding steps: 
    1. Sign the mandate (view/download and sign electronically or upload a signed copy).
    2. Upload ID and proof of residence.
    3. Complete onboarding.
    """
    client_id = st.session_state.client_id
    client_info = clients_data.get(client_id, {})

    st.subheader(f"Welcome, {client_info.get('name', '')}")
    st.write("Please complete the onboarding process below.")

    # STEP 1: Mandate signature
    st.header("Step 1: Mandate Signature")

    # Display the mandate PDF for viewing or downloading
    with open(MANDATE_FILE_PATH, "rb") as mandate_file:
        st.download_button(
            label="Download Mandate PDF",
            data=mandate_file,
            file_name="AM_LAW_INC_FICA_FEE_MANDATE_2025.pdf",
            mime="application/pdf",
        )
    
    st.write("Please review the mandate before proceeding.")
    
    # Options for signing the mandate
    sign_option = st.selectbox(
        "Choose how you will sign the mandate:",
        ["Select an option", "E-sign", "Upload scanned copy"]
    )

    e_sign_complete = False
    mandate_uploaded = False

    # E-SIGN
    if sign_option == "E-sign":
        st.write("**E-sign the mandate**")
        signature = st.text_input("Type your full name as your electronic signature:")
        confirm = st.checkbox("I confirm that this is my signature and I agree to the terms of the mandate.")
        
        if signature and confirm:
            st.success("E-signature captured!")
            e_sign_complete = True

    # UPLOAD SCANNED COPY
    elif sign_option == "Upload scanned copy":
        st.write("Upload the signed copy of the mandate.")
        signed_mandate = st.file_uploader(
            "Upload Signed Mandate (PDF, JPG, PNG, etc.)", 
            type=["pdf", "jpg", "jpeg", "png"]
        )
        if signed_mandate:
            st.success("Mandate uploaded successfully!")
            mandate_uploaded = True

    # STEP 2: Upload ID and Proof of Residence
    st.header("Step 2: Upload ID and Proof of Residence")

    uploaded_id = st.file_uploader(
        "Upload a copy of your ID (PDF, JPG, PNG)", 
        type=["pdf", "jpg", "jpeg", "png"]
    )
    uploaded_proof = st.file_uploader(
        "Upload a copy of your Proof of Residence (PDF, JPG, PNG)", 
        type=["pdf", "jpg", "jpeg", "png"]
    )

    # Check if we can complete the onboarding
    if (e_sign_complete or mandate_uploaded) and uploaded_id and uploaded_proof:
        if st.button("Complete Onboarding"):
            reference_id = str(uuid.uuid4())

            st.success("Onboarding Completed!")
            st.write(f"Reference ID: `{reference_id}`")
            st.write("Thank you for completing your onboarding process.")

            # Optionally log the user out or reset state
            st.session_state.logged_in = False
            st.session_state.client_id = None


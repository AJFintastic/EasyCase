import streamlit as st
from login import show_login
from onboard import show_onboarding
from ai_legal_assistant import show_legal_assistant

# Initialize session state for login if not set
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "client_id" not in st.session_state:
    st.session_state.client_id = None

def logout():
    st.session_state.logged_in = False
    st.session_state.client_id = None
    st.rerun()

def main():
    st.title("⚖️ AM Law Inc - Client Portal")

    # If the user is NOT logged in, show the login page only.
    if not st.session_state.logged_in:
        show_login()
        return  # Prevent sidebar from appearing

    # Sidebar with navigation and logout button
    st.sidebar.title("Navigation")
    # Define pages with icons
    pages = {
        "🏠 Onboarding": "Onboarding",
        "🤖 Legal AI Advisor": "Legal AI Advisor"
    }
    selected_page = st.sidebar.selectbox("Go to", list(pages.keys()))
    
    # Add spacing and a logout button at the bottom of the sidebar
    st.sidebar.markdown("---")
    if st.sidebar.button("🔓 Logout"):
        logout()

    # Page routing
    page = pages[selected_page]
    if page == "Onboarding":
        show_onboarding()
    elif page == "Legal AI Advisor":
        show_legal_assistant()

if __name__ == "__main__":
    main()

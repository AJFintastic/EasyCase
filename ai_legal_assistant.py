import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import concurrent.futures  # For parallel API calls

# Load environment variables
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize model
model = genai.GenerativeModel('gemini-pro')

# South African Legal parameters
SA_CASE_TYPES = [
    "Labour Dispute", "Land Reform", "BEE Compliance",
    "Family Law", "Criminal Law", "Consumer Protection",
    "Mining Rights", "Customary Law", "Immigration",
    "Contract Law", "Estate Planning"
]

SA_JURISDICTIONS = [
    "Constitutional Court", "Supreme Court of Appeal",
    "High Court", "Magistrate's Court",
    "Labour Court", "Land Claims Court",
    "Gauteng", "Western Cape", "KwaZulu-Natal",
    "Eastern Cape", "Limpopo", "Mpumalanga"
]

# ---------------------------
# Helper: Initialize Session State Keys
# ---------------------------
def initialize_session_state():
    keys_defaults = {
        "report_generated": False,
        "generated_sections": [],
        "case_type": SA_CASE_TYPES[0],
        "jurisdiction": SA_JURISDICTIONS[0],
        "legal_question": "",
        "involved_parties": "",
        "existing_docs": ""
    }
    for key, default in keys_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

# ---------------------------
# SA Legal styling
# ---------------------------
st.markdown("""
<style>
    .legal-box {
        background: #F8FAFF;
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #007749;
        box-shadow: 0 2px 4px rgba(0,119,73,0.1);
    }
    .section-header {
        color: #001489;
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 1.2em;
        margin-bottom: 12px;
    }
    .analysis-box {
        background: #E8F4F0;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        line-height: 1.6;
    }
    .disclaimer-box {
        background: #FFF5F5;
        border: 2px solid #DE3831;
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# AI Legal Analysis Function
# ---------------------------
def get_legal_analysis(prompt, case_type, jurisdiction, legal_question, involved_parties, existing_docs):
    try:
        legal_context = f"""
        South African Legal Matter:
        - Case Type: {case_type}
        - Jurisdiction: {jurisdiction}
        - Involved Parties: {involved_parties}
        - Existing Documentation: {existing_docs}

        Legal Question:
        {legal_question}

        Analysis Requirements ({prompt}):
        - Reference relevant SA Acts and Regulations
        - Consider Constitutional Court rulings
        - Include practical court procedure guidance
        - Note provincial legal variations if applicable
        - Suggest local legal aid resources
        """
        response = model.generate_content(legal_context)
        return response.text
    except Exception as e:
        st.error(f"Legal AI Error: {str(e)}")
        return None

# ---------------------------
# Form Reset Function
# ---------------------------
def clear_form():
    st.session_state.report_generated = False
    st.session_state.generated_sections = []
    st.session_state.case_type = SA_CASE_TYPES[0]
    st.session_state.jurisdiction = SA_JURISDICTIONS[0]
    st.session_state.legal_question = ""
    st.session_state.involved_parties = ""
    st.session_state.existing_docs = ""

# ---------------------------
# Main Function: Display the AI Legal Assistant page
# ---------------------------
def show_legal_assistant():
    """
    Display the AI Legal Assistant page.
    """
    # Ensure session state keys are initialized
    initialize_session_state()

    st.title("🤖 AM Law AI Advisor 🤖")
    st.markdown("---")
    
    # Input Section
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Case Type 📂", SA_CASE_TYPES, key="case_type")
    with col2:
        st.selectbox("Jurisdiction 🌍", SA_JURISDICTIONS, key="jurisdiction")
        
    st.text_area("Legal Question ❓", key="legal_question", height=150,
                 placeholder="E.g.: 'Can a traditional leader claim mineral rights under MPRDA?'")
    st.text_area("Involved Parties 👥", key="involved_parties",
                 placeholder="Include companies/IDs if applicable")
    st.text_area("Existing Documentation 📑", key="existing_docs",
                 placeholder="E.g.: BEE Certificate, Employment Contract, Title Deed")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        generate_clicked = st.button("🔍 Analyze Case")
    with col2:
        clear_clicked = st.button("🧹 Clear Form", on_click=clear_form)
    
    if generate_clicked:
        if not st.session_state.legal_question or not st.session_state.case_type:
            st.error("❌ Please provide at least a legal question and case type")
            st.stop()
        
        try:
            with st.spinner("⚖️ Consulting SA legal frameworks..."):
                sections = [
                    {"title": "Framework", "prompt": "Identify applicable SA laws and regulations"},
                    {"title": "Case Law", "prompt": "Reference relevant Constitutional Court and High Court decisions"},
                    {"title": "Provinces", "prompt": "Highlight jurisdiction-specific requirements"},
                    {"title": "Process", "prompt": "Outline required forms and court processes"},
                    {"title": "Legal Aid", "prompt": "Suggest legal aid clinics and pro bono services"}
                ]
                
                # Copy session state values into local variables
                local_case_type = st.session_state.case_type
                local_jurisdiction = st.session_state.jurisdiction
                local_legal_question = st.session_state.legal_question
                local_involved_parties = st.session_state.involved_parties
                local_existing_docs = st.session_state.existing_docs

                # Run the API calls concurrently using local variables
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    responses = list(executor.map(
                        lambda sec: get_legal_analysis(
                            sec["prompt"],
                            local_case_type,
                            local_jurisdiction,
                            local_legal_question,
                            local_involved_parties,
                            local_existing_docs
                        ),
                        sections
                    ))
                
                generated_sections = []
                for section, response in zip(sections, responses):
                    if not response:
                        st.error(f"Failed to generate legal analysis for {section['title']}")
                        st.stop()
                    generated_sections.append({
                        "title": section["title"],
                        "content": response
                    })
                
                st.session_state.generated_sections = generated_sections
                st.session_state.report_generated = True
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.session_state.report_generated = False
    
    if st.session_state.report_generated:
        st.markdown("---")
        # Icon mapping for tabs
        icon_mapping = {
            "Framework": "📜",
            "Case Law": "🏛️",
            "Provinces": "🗺️",
            "Process": "📝",
            "Legal Aid": "🤝"
        }
        tab_titles = [f"{icon_mapping[section['title']]} {section['title']}" for section in st.session_state.generated_sections]
        tabs = st.tabs(tab_titles)
        
        for idx, tab in enumerate(tabs):
            with tab:
                section = st.session_state.generated_sections[idx]
                st.markdown(f'''
                <div class="legal-box">
                    <h3 class="section-header">{section["title"]}</h3>
                    <div class="analysis-box">
                        {section["content"]}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown('''
        <div class="disclaimer-box">
            <h3>⚠️ Legal Disclaimer</h3>
            <p>This AI tool does not constitute legal advice. Consult a registered legal practitioner.</p>
        </div>
        ''', unsafe_allow_html=True)

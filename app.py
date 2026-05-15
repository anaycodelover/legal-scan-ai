import streamlit as st
from groq import Groq
import PyPDF2

# 1. Page Configuration (The Premium Look)
st.set_page_config(page_title="LegalScan Pro", page_icon="⚖️", layout="centered")

# Custom CSS for Dark Mode & Clean UI
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #1e1e1e; color: #00ffa3; border: 1px solid #3d3d3d; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ LegalScan Pro")
st.caption("AI Litigation Intelligence for Boutique Law Firms")

# 2. Sidebar for Configuration
with st.sidebar:
    st.header("Settings")
    user_api_key = st.text_input("Enter Groq API Key", type="password")
    uploaded_file = st.file_uploader("Upload Deposition (PDF)", type="pdf")

# 3. Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about the document..."):
    if not user_api_key:
        st.error("Please enter your API Key in the sidebar!")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Processing
        client = Groq(api_key=user_api_key)
        
        # Extract text if file exists
        doc_text = ""
        if uploaded_file:
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                doc_text += page.extract_text()

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"You are a legal expert. Use this transcript to answer questions: {doc_text[:10000]}"},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.1-70b-versatile",
            )
            response = stream.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

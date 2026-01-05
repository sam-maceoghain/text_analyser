import os
import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv
### from pypdf import PdfReader
import pdfplumber

# 1. Setup & Configuration
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)

# 2. Interface
st.title("CV vs Job Description")
st.markdown("### Upload your CV to compare against selected Job Description using Claude AI")

col1, col2 = st.columns(2) # -->

# 2.1 Job Description
with col1:
    job_text = st.text_area("Paste Job Description:", height=300)

# 2.2 CV Upload
with col2:
    uploaded_file = st.file_uploader("Upload your CV (PDF):", type=["pdf"])

    # Initialise empty variable
    cv_text = "" 
    if uploaded_file is not None:
        # pdfplumber implementation
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    cv_text += text

            # Print success message
            st.success(f"CV loaded successfully - ({len(cv_text)} characters)")
            # Preview CV Text
            with st.expander("Preview CV Text"):
                st.write(cv_text)

        except Exception as e:
            st.error(f"Error reading PDF file: {e}")

#------------------------
# The Logic (Backend)
#------------------------


#------------------------
# The Logic (Backend)
#------------------------

# The Analyse Button
if st.button("Analyse"):
    if not job_text or not cv_text:
        st.warning("Please paste the Job Description & Upload your CV")
    else:
        with st.spinner('Analysing...'):
            try:
                # The comparison prompt
                message = client.messages.create(
                    model="claude-3-haiku-20240307", 
                    max_tokens=300,
                    messages=[
                        {
                            "role": "user",

                            "content": f"""
                            
                            You are an expert Technical Recruiter and ATS Optimisation Specialist. 

                            Analyse the following CV against the provided Job Description (JD).

                            ---
                            CANDIDATE CV:
                            {cv_text}

                            ---
                            JOB DESCRIPTION:
                            {job_text}

                            Produce a strict, data-driven report with the following three sections:

                            ### 1. ATS Match Score & Rationale
                            - Provide a match percentage (0-100%)
                            - Do not be polite. Be objective

                            ### 2. The Gap Analysis
                            - List technical tools/languages present in the JD but completely missing from the CV
                            - List behavioral traits emphasised in the JD but absent in the CV

                            ###3. High Impact Improvements
                            - Identify the 3 weakest bullet points in the CV regarding this specific JD

                            Output Requirement: be concise, blunt, and directive (UK English)
                            """
                        }
                    ]
                )

                # Display the AIs response
                st.write("### Analysis Report")
                ### response_text = message.content[0].text
                st.write(message.content[0].text)

            except Exception as e:
                st.error(f"An error occurred: {e}")
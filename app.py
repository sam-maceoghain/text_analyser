# ----------------
# Libraies
# ----------------

import pdfplumber # --> replaces pypdf (more complex cv designs)
import os
import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv

# ----------------
# Setup & Configuration
# ----------------

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)

# ----------------
# Interface
# ----------------

# Title & Description
st.title("CV vs Job Description")
st.markdown("### Compare your CV against selected Job Description using Claude AI")

# Two columns layout
col1, col2 = st.columns(2)

# 2.1 CV Upload
with col1:
    uploaded_cv = st.file_uploader("Upload your CV (PDF):", type=["pdf"])

    # Initialise empty variable
    cv_text = "" 
    if uploaded_cv is not None:
        try:
            with pdfplumber.open(uploaded_cv) as pdf: # --> pdfplumber implementation
                for page in pdf.pages:
                    text = page.extract_text()
                    cv_text += text

            # Success message
            st.success(f"CV loaded - ({len(cv_text)} characters)")

            # Preview CV text
            with st.expander("Preview CV Text"):
                st.write(cv_text)

        except Exception as e:
            st.error(f"Error reading PDF file: {e}")

# 2.2 Job Description
with col2:
    job_text = st.text_area("Paste Job Description:", height=300)

#------------------------
# The Logic (Backend)
#------------------------

# The button
if st.button("Analyse"):
    if not job_text or not cv_text:
        st.warning("Please insert the job description &/or upload your CV")
    else:
        with st.spinner('Analysing...'):
            try:
                # The comparison prompt
                message = client.messages.create(
                    model="claude-3-haiku-20240307", 
                    max_tokens=800,
                    messages=[
                        {
                            "role": "user",

                            "content": f"""

                            Act as a strict Technical Recruiter. Compare this CV against the Job Description.
                            
                            Output a concise and direct 3-part report (UK English):

                            ### 1. Match Score
                            - Give a strict %.
                            - One sentence explaining the score.

                            ### 2. Missing Skills
                            - List the specific technical tools or key soft skills missing from the CV.
                            - Bullet points only. Direct and blunt.

                            ### 3. High Impact Improvements
                            - Identify the 3 weakest bullet points in the CV.
                            - Rewrite them instantly to match the Job Description.

                            ---
                            CANDIDATE CV:
                            {cv_text}

                            ---
                            JOB DESCRIPTION:
                            {job_text}

                            """
                        }
                    ]
                )

                # Display the AIs response
                st.write("### Analysis Report")
                st.write(message.content[0].text)

            except Exception as e:
                st.error(f"An error occurred: {e}")
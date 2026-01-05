import os
import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv

#------------------------
# Setup & Configuration
#------------------------

# Load API key from .env file
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key) 

#------------------------
# The Interface
#------------------------

# Title on the screen
st.title("CV vs Job Description")
st.markdown("### Attach your CV & selected Job Description to see the match percentage using Claude AI")

# Create two columns for side-by-side inputs
col1, col2 = st.columns(2)

with col1:
    # Text box for CV input
    cv_text = st.text_area("Paste your CV here:", height=300)

with col2:
    # Text box for Job Description input
    job_text = st.text_area("Paste Job Description here:", height=300)

#------------------------
# The Logic (Backend)
#------------------------

# The Analyse Button
if st.button("Analyse"):
    if not cv_text or not job_text:
        st.warning("Please enter both your CV & the Job Description to analyse")
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
                            
                            Compare the following CV & Job Description. 

                            Output a strict report in three sections:

                            1. Match Score: Provide an honest match percentage based on skills + experience match.

                            2. Missing Skills: List key skills required by the Job Description that are absent in the CV.

                            3. Suggested Improvements: Recommend how the CV can be improved - how it can be rephrased to better match this specific job. 

                            ---
                            JOB DESCRIPTION:
                            {job_text}
                            1. Match Score: Provide an honest match percentage based on skills + experience match.

                            2. Missing Skills: List key skills required by the Job Description that are absent in the CV.

                            3. Suggested Improvements: Recommend how the CV can be improved - how it can be rephrased to better match this specific job. 

                            ---
                            JOB DESCRIPTION:
                            {job_text}

                            ---
                            CANDIDATE CV:
                            {cv_text}
                            """
                        }
                    ]
                )

                # Display the AIs response
                st.subheader("Analysis Report")
                response_text = message.content[0].text
                st.write(response_text)

            except Exception as e:
                st.error(f"An error occurred: {e}")


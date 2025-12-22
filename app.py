#------------------------
#
#------------------------
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

# Create a client object to interact with the Anthropic API
# This object handles communication with the API
client = Anthropic(api_key=api_key)

#------------------------
# The Interface
#------------------------

# Title on the screen
st.title("AI Text Analyser")
st.markdown("### Extract Keywords & Skills from Job Descriptions using Claude AI")

# Create a text box for user input
text_input = st.text_area("Paste Job Description:", height=200)

#------------------------
# The Logic (Backend)
#------------------------

# The Analyse Button
# When the button is clicked, process the user input text
if st.button("Analyse"):
    
    # Validation: Check if text input is empty
    if not text_input:
        st.warning("Please enter some text to analyse")

    # If text input is provided, proceed with analysis    
    else:
        # Spinning cirlce to indicate processing
        with st.spinner('Claude is thinking...'):
            try:
           
                # The API Call
                # This is where we actually send data to the AI
                message = client.messages.create(
                    model="claude-3-haiku-20240307", 
                    max_tokens=200, 
                    messages=[
                        {
                        "role": "user",
                        # The Prompt Engineering
                        "content": f"Analyse this job description. Briefly list:\n1. Key Skills (Technical & Soft)\n2. Required Experience (Years/Level)\n3. Top Keywords to include in my CV for the ATS.\n\nJob Description:\n{text_input}"
                        }
                    ]
                )

                # Display the response from the AI on the screen
                response_text = message.content[0].text
                st.write("### Analysis Results")
                st.write(response_text)
            
            except Exception as e:
                st.error(f"An error occurred: {e}")
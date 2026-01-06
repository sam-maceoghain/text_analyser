# ----------------
# Libraies
# ----------------

import base64
import fitz # --> PyMuPDF (Image Conversion)
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

# Funciton
def pdf_to_base64_images(uploaded_file):
    """Converts PDF pages to a list of Base64 encoded images"""
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    image_list = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        # Convert page to an image (PNG)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # --> Zoom=2 for higher quality
        img_data = pix.tobytes("png")
        # Encode image to Base64 for the API
        base64_str = base64.b64encode(img_data).decode('utf-8')
        image_list.append(base64_str)

    return image_list

# ----------------
# Interface
# ----------------

# Title & Description
st.title("CV Matcher (Vision Edition)")
st.markdown("### Upload your CV. The AI will read it like a human.")

# Two columns layout
col1, col2 = st.columns(2)

# 2.1 CV Upload
with col1:
    uploaded_cv = st.file_uploader("Upload your CV (PDF):", type=["pdf"])

    # Initialise empty list
    cv_images = [] 
    if uploaded_cv is not None:
        try:
            # Convert PDF to Images immediately
            cv_images = pdf_to_base64_images(uploaded_cv) # --> function call
            # Success message
            st.success(f"CV processed - ({len(cv_images)} pages converted to images)")
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
    if not job_text or not cv_images:
        st.warning("Please insert the job description &/or upload your CV")
    else:
        with st.spinner('Analysing visual layout & content...'):
            try:

                # Prepare the message payload with images
                content_payload = []

                # 1. Add instructions
                instruction_text = f"""
                Act as a strict Technical Recruiter. You are looking at images of a candidate's CV.
                Compare the skills visible in the images against the Job Description provided.
                ---
                JOB DESCRIPTION:
                {job_text}

                Output a concise, realistic and direct 3-part report (UK English):
                1. Match Score (%)
                2. Missing Skills (Analyse the images carefully for technical keywords)
                3. High Impact Improvements
                """

                content_payload.append({"type": "text", "text": instruction_text})

                # 2. Add the images

                for img_str in cv_images:
                    content_payload.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": img_str
                        }           
                    })
                
                # Send the message to the API (Claude)
                message = client.messages.create(
                    model="claude-3-haiku-20240307", 
                    max_tokens=800,
                    messages=[
                        {
                            "role": "user",
                            "content": content_payload
                        }
                    ]
                )

                # Display the AIs response
                st.write("### Analysis Report")
                st.write(message.content[0].text)

            except Exception as e:
                st.error(f"An error occurred: {e}")
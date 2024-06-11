from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

# Load environment variables
load_dotenv()

# Configure the API key for the generative model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="ATS Resume Tracker")


def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, pdf_content, prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    images = pdf2image.convert_from_bytes(uploaded_file.read())
    first_page = images[0]
    
    img_byte_arr = io.BytesIO()
    first_page.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
        
    pdf_parts = {
        "mime_type": "image/jpeg",
        "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
    }
    return pdf_parts

# # Add background image CSS
# def add_bg_from_url():
#     st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             background: url("https://i.ytimg.com/vi/w5yhHUoJa2M/maxresdefault.jpg");
#             background-size: cover;
#             background-repeat: no-repeat;
#             background-attachment: fixed;
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# # Add background image
# add_bg_from_url()


st.markdown(
    """
    <marquee width="80%" direction="right" height="150px" style="text-align:center;">
        <br><br>
        <h3 style="font-size: 50px">ATS Tracking System</h3> 
    </marquee>
    """,
    unsafe_allow_html=True
)
input_text = st.text_area("Job Description", key="input_text")
uploaded_file = st.file_uploader("Upload Your Resume (in PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
Also mention the views of HR perpective on this resume.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First, the output should come as a percentage, then keywords missing, and lastly, final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

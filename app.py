from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import fitz  # PyMuPDF
import google.generativeai as genai
import io
import base64

# Load environment variables
load_dotenv()

# Configure the API key for the generative model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="ATS Resume Tracker")

def get_gemini_response(input_text, pdf_images, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, *pdf_images, prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    images = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img_byte_arr = io.BytesIO()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        images.append({
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        })
        
    return images

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
uploaded_file = st.file_uploader("Upload Your Resume (in PDF)...  ((USE ONLY SINGLE PAGE RESUME ))", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
Also mention the views of HR perspective on this resume.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First, the output should come as a percentage, then keywords missing, and lastly, final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
            st.subheader("The Response is")
            st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            response = get_gemini_response(input_text, pdf_content, input_prompt3)
            st.subheader("The Response is")
            st.write(response)
    else:
        st.write("Please upload the resume")

# Footer setup (unchanged)
import streamlit as st
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)

def layout(*args):
    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """
    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="white",
        text_align="center",
        height="auto",
        opacity=1
    )
    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )
    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )
    st.markdown(style, unsafe_allow_html=True)
    for arg in args:
        if isinstance(arg, str):
            body(arg)
        elif isinstance(arg, HtmlElement):
            body(arg)
    st.markdown(str(foot), unsafe_allow_html=True)

def footer():
    myargs = [
        "Made with "
        " ❤️  by",
        link("https://github.com/ayushdit03", "@AyushJain"),
        "&nbsp;&nbsp;&nbsp;",
        link("https://www.linkedin.com/in/ayush-jain-8b6985231", image('https://tse1.mm.bing.net/th?id=OIP.qgMyI8LMGST1grqseOB85AAAAA&pid=Api&P=0&h=220', width=px(25), height=px(25))),
    ]
    layout(*myargs)

if __name__ == "__main__":
    footer()

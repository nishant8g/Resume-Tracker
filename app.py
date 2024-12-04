from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
from PyPDF2 import PdfReader
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to generate response using Gemini
def get_gemini_response(input_text, pdf_text, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_text, prompt])
    return response.text

# Function to extract text from PDF using PyPDF2
def extract_text_from_pdf(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise RuntimeError(f"Error reading PDF: {e}")

# Streamlit app setup
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF uploaded successfully!")

# Buttons for different functionalities
submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improve my Skills")
submit3 = st.button("Percentage Match")

# Prompts for each button
input_prompt1 = """
You are an experienced professional with tech expertise in Data Science, Full Stack Web Development, Big Data Engineering, DevOps, and Data Analysis. 
Your task is to review the provided resume against the job description for all profiles. Please share your professional evaluation on whether the candidate's 
profile aligns with the requirements, highlighting strengths and weaknesses.
"""

input_prompt2 = """
Based on the candidate's current skills and experience, offer actionable suggestions for improvement in areas such as Data Science, Full Stack Web Development, 
Big Data Engineering, DevOps, and Data Analysis. Recommend relevant courses, certifications, and projects to enhance expertise, and highlight key technical 
skills and tools in demand. Advise on building a portfolio, networking, and staying updated with industry trends for career growth.
"""

input_prompt3 = """
Calculate the alignment percentage between the candidate's resume and the job description. Provide a breakdown of strengths, areas for improvement, and 
factors influencing the match percentage, helping the candidate understand their compatibility with the job requirements.
"""

# Action for each button
if submit1:
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        response = get_gemini_response(input_text, pdf_text, input_prompt1)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.error("Please upload a file")

elif submit2:
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        response = get_gemini_response(input_text, pdf_text, input_prompt2)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.error("Please upload a file")

elif submit3:
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        response = get_gemini_response(input_text, pdf_text, input_prompt3)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.error("Please upload a file")

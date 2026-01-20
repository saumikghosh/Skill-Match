import streamlit as st
from pdfextracter import text_extracter
from langchain_google_genai import ChatGoogleGenerativeAI
import os
# First, let's configure the model
gemini_api_key = os.getenv('GOOGLE-API-19jan-key2')
# Change 'model_name' to 'model'
model = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash-lite',  # Standardized parameter
    temperature=0.9,
    api_key=gemini_api_key
)
# create the main page of the application
st.title(":orange[Skill Match:] :blue[An AI Powered Application]",width="content")
st.sidebar.title(":green[Upload Your Resume (only PDF)]")
file = st.sidebar.file_uploader("Upload your resume here", type=["pdf"])
if file:
    file_text = text_extracter(file)
    st.sidebar.success("Resume uploaded successfully!")
st.markdown("#### :red[Upload your resume and job description to find the appropriate match!]",width="content")
tips = '''
Follow these steps:
1. Upload your resume in the sidebar (pdf only).
2. copy and paste the job description below.
3. Click on Submit to run the app.'''
st.write(tips)
job_desc = st.text_area(":violet[Copy & Paste your Job Description over here:]", height=250, key="job_desc",max_chars=70000)
if st.button('Submit'):
    prompt = f""" 
    <Role> You are an expert in analyzing resume and matching it with job descriptions.
    <Goal> Match the resume and the job description provided by the applicant.
    <Context> The following content has been provided by the applicant.
    * Resume: {file_text}
    * Job description: {job_desc}
    <Format> The report should follow these steps:
    * Give a brief description of the applicant in 3 to 5 lines.
    * Describe the percentage what are the chances of this resume getting selected.
    * Need not to be the exact percentage, you can give interval of percentage.
    * List out the relevant skills from the resume that match the job description.
    * List out the missing skills that are in the job description but not in the resume.
    * Give the expected ATS score.
    * Perform SWOT Analysis and explain each parameter i.e. strength, weakness, Opportunity and Threat. When a new section or sentence starts don't write <br>
    * Give what all sections in the current resume are required to be improved in order to improve selection percent and ATS score.
    * Show both current version and improved version of resume sections.
    * Create two sample resume which can maximise the ATS score and selection percent.
    <Instruction> Use bullet points for explanation wherever possible. Create tables for description wherever required. Strictly do not add any new skill in sample resume. The format of the sample resume must be such that they can be copied or pasted directly on MS-Word.
    """

    with st.spinner("Analyzing the resume and job description..."):
        response = model.invoke(prompt)
        st.write(response.content)
    

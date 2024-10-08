import os
from src.chain import Chain
from src.vector_db import VectorDB
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from src.utils import convert_to_latex, write_to_latex_file, untangle_job_data
import json

load_dotenv()

if "chain" not in st.session_state:
    st.session_state.chain = Chain(0, os.getenv("GROQ_API_KEY"), os.getenv("MODEL"))
    st.session_state.vector_db = VectorDB("vectorstore", "job_description")
    st.session_state.vector_db.add_data("data/experience.json")

def create_streamlit_app():
    st.title("Cover Letter Generator")
    st.markdown("This app generates cover letters based on job descriptions.")
    url_input = st.text_input("Enter the URL of the job description page:")
    submit_button = st.button("Submit")
    resume_button = st.button("Generate Resume")

    if (submit_button or resume_button) and url_input:
        if not url_input.startswith("http"):
            page_data = url_input
        else:
            loader = WebBaseLoader(url_input)
            page_data = loader.load().pop().page_content
        job_details = st.session_state.chain.extract_job_details(page_data)
        if len(job_details) == 0:
            st.write("Unable to scrape job data from the provided URL.")
        else:
            chroma_query = st.session_state.chain.create_query(page_data)
            job_data = st.session_state.vector_db.search(chroma_query)

            if resume_button:
                resume_points = st.session_state.chain.generate_resume_points(job_details['role'], job_details['company_name'], job_details['job_description'], job_data)
                resume_points = json.loads(resume_points)
                # print("Keys: ", resume_points.keys())
                # print(resume_points)
                st.write(resume_points)
                write_to_latex_file(convert_to_latex(resume_points), job_details['company_name'])
            else:
                cover_letter = st.session_state.chain.generate_cover_letter(job_details['role'], job_details['job_description'], job_details['company_name'], job_data)
                st.write(cover_letter)

if __name__ == "__main__":
    create_streamlit_app()

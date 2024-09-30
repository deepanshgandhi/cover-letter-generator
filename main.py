import os
from src.chain import Chain
from src.vector_db import VectorDB
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from IPython import embed

load_dotenv()

if "chain" not in st.session_state:
    st.session_state.chain = Chain(0, os.getenv("GROQ_API_KEY"), os.getenv("MODEL"))
    st.session_state.vector_db = VectorDB("vectorstore", "job_description")
    st.session_state.vector_db.add_data("data/experience.json")

def create_streamlit_app():
    st.title("Cover Letter and Resume Generator")
    st.markdown("This app generates cover letters based on job descriptions.")
    url_input = st.text_input("Enter the URL of the job description page:")
    
    generate_cover_letter_button = st.button("Generate Cover Letter and resume")
    
    if generate_cover_letter_button and url_input:
        if not url_input.startswith("http"):
            page_data = url_input
        else:
            loader = WebBaseLoader(url_input)
            page_data = loader.load().pop().page_content
        job_details = st.session_state.chain.extract_job_details(page_data)
        print('\n Job details: \n', job_details)
        if len(job_details) == 0:
            st.write("Unable to scrape job data from the provided URL.")
        else:
            chroma_query = st.session_state.chain.create_query(page_data)
            print('\n Chroma query: ', chroma_query)
            job_data = st.session_state.vector_db.search(chroma_query)
            print(job_data)
            #print(st.session_state.vector_db.search_by_company(chroma_query, "Speridian Technologies"))
            cover_letter = st.session_state.chain.generate_cover_letter(job_details['role'], job_details['job_description'], job_details['company_name'], job_data)
            resume = st.session_state.chain.generate_resume(job_details['job_description'], job_data)
            print(resume)
            st.write(cover_letter)
            #st.write(resume)



if __name__ == "__main__":
    create_streamlit_app()

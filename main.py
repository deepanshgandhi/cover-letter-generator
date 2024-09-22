import os
from src.chain import Chain
from src.vector_db import VectorDB
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader

load_dotenv()

def create_streamlit_app(chain, vector_db):
    st.title("Cover Letter Generator")
    st.markdown("This app generates cover letters based on job descriptions.")
    url_input = st.text_input("Enter the URL of the job description page:")
    submit_button = st.button("Submit")
    if submit_button:
        loader = WebBaseLoader(url_input)
        page_data = loader.load().pop().page_content
        job_details = chain.extract_job_details(page_data)
        chroma_query = chain.create_query(url_input)
        job_data = vector_db.search(chroma_query)
        cover_letter = chain.generate_cover_letter(job_details[0]['job_description'], job_details[0]['company_name'], job_data)
        st.write(cover_letter)

if __name__ == "__main__":
    chain = Chain(0, os.getenv("GROQ_API_KEY"), os.getenv("MODEL"))
    vector_db = VectorDB("vectorstore", "job_description")
    vector_db.add_data("data/experience.json")
    create_streamlit_app(chain, vector_db)

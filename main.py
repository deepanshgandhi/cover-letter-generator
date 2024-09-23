import os
from src.chain import Chain
from src.vector_db import VectorDB
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader

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

    if submit_button and url_input:
        loader = WebBaseLoader(url_input)
        page_data = loader.load().pop().page_content
        job_details = st.session_state.chain.extract_job_details(page_data)
        chroma_query = st.session_state.chain.create_query(url_input)
        print(chroma_query)
        job_data = st.session_state.vector_db.search(chroma_query)
        print(job_data)
        print(job_details)
        #print(page_data)
        #print(st.session_state.vector_db.search_by_company(chroma_query, "Speridian Technologies"))
        cover_letter = st.session_state.chain.generate_cover_letter(job_details[0]['job_description'], job_details[0]['company_name'], job_data)
        st.write(cover_letter)

if __name__ == "__main__":
    create_streamlit_app()

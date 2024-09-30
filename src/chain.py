from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from config import job_detail_prompt, create_chromadb_query_prompt, generate_cover_letter_prompt, generate_resume_prompt

class Chain:
    def __init__(self, temperature, groq_api_key, model_name):
        self.temperature = temperature
        self.groq_api_key = groq_api_key
        self.model_name = model_name
        self.llm = ChatGroq(
            temperature=self.temperature,
            groq_api_key=self.groq_api_key,
            model_name=self.model_name
        )
    
    def extract_job_details(self, page_content):
        prompt_extract = PromptTemplate.from_template(
            job_detail_prompt
        )
        
        chain_extract = prompt_extract | self.llm 
        res = chain_extract.invoke(input={'page_content':page_content})
        try:
            json_parser = JsonOutputParser()
            return json_parser.parse(res.content)
        except OutputParserException as e:
            raise OutputParserException("Unable to parse jobs.")
        return {}
    
    def create_query(self, page_content):
        prompt_extract = PromptTemplate.from_template(
            create_chromadb_query_prompt
        )
        chain_extract = prompt_extract | self.llm 
        chroma_query = chain_extract.invoke(input={'page_content':page_content})
        return chroma_query.content
    
    def generate_cover_letter(self, job_title, job_description, company_name, experience_list):
        cover_letter_prompt = PromptTemplate.from_template(
            generate_cover_letter_prompt
        )

        chain_email = cover_letter_prompt | self.llm
        res = chain_email.invoke({
        "job_title": job_title,
        "job_description": job_description,
        "company_name": company_name,
        "experience_list" : experience_list
        }
        )
        return res.content
    
    def generate_resume(self, experience_list, job_description):
        with open('data/resume.tex', 'r') as f:
            resume = f.read()
        
        resume_prompt = PromptTemplate.from_template(
            generate_resume_prompt
        )

        chain_email = resume_prompt | self.llm
        res = chain_email.invoke({
        "resume": resume,
        "experience_list" : experience_list,
        "job_description": job_description
        }
        )
        return res.content
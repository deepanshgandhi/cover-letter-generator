from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

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
                """
                ### SCRAPED TEXT FROM WEBSITE:
                {page_content}
                ### INSTRUCTION:
                The scraped text is from the career's page of a website.
                Your job is to extract the job postings and return them in JSON format containing the 
                following keys: `role`, `company_name`, `experience`, `skills` and `job_description`,
                where the job description provides detailed information about the job responsibilities and expectations.
                Ensure that the role is straightforward.
                Only return the valid JSON.
                ### VALID JSON (NO PREAMBLE):    
                """
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
                """
                ### SCRAPED TEXT FROM WEBSITE:
                {page_content}
                ### INSTRUCTION:
                The scraped text is from the career's page of a website.
                Your task is to analyze the job description and generate a relevant query to fetch matching data from Chroma DB.
                The query should focus on extracting key responsibilities, required skills, and any specific roles mentioned in the description.
                Ensure that the query is concise and effectively captures the essential elements needed for a targeted search in Chroma DB.
                Only return the generated query text.
                ### VALID JSON (NO PREAMBLE):    
                """
        )
        chain_extract = prompt_extract | self.llm 
        chroma_query = chain_extract.invoke(input={'page_content':page_content})
        return chroma_query.content
    
    def generate_cover_letter(self, job_description, company_name, experience_list):
        cover_letter_prompt = PromptTemplate.from_template(
            """Your name is Deepansh Gandhi, and you are currently a Machine Learning Intern at Staples while pursuing a Masters 
            in Artificial Intelligence at Northeastern University. Using the job description provided below, write a tailored cover letter 
            for the company. Make the tone professional, yet enthusiastic, showcasing how your experience aligns with the job requirements.

        Job Description: {job_description}
        Company Name: {company_name}

        Include the following:

        Introduction: Start by expressing your interest in the position and the company, and briefly mention your current role at Staples 
        and academic background at Northeastern University.
        Relevant Experience: From your list of past work experiences, highlight the most relevant points that align with the job description 
        at {company_name}. The experiences provided below should be woven into the narrative naturally, 
        showcasing how your skills are a direct match for what the company is looking for.
        Skills & Achievements: Emphasize your technical skills, particularly in machine learning, data processing, and other areas 
        that are valuable for the role. Mention any standout achievements in your internships or projects, quantifying impact when possible.
        Company Fit: Convey your understanding of the company's mission and how it resonates with your personal and professional goals.
        Discuss how you can contribute to their team or how the role fits into your career aspirations.
        Closing: Reiterate your enthusiasm for the role, express interest in an interview, and thank them for considering your application.
        Experience List: {experience_list}"""
        )

        chain_email = cover_letter_prompt | self.llm
        res = chain_email.invoke({"job_description": job_description,
        "company_name": company_name,
        "experience_list" : experience_list
        }
        )
        return res.content
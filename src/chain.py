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
                Only use the information which is present in the page.
                Only return the valid JSON.
                It should not be a list. It should be a single JSON object.
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
            """Your name is Goutham Yadavalli, pursuing a Master's in Computer Science at Northeastern University. Based on the job description below, write a concise and tailored cover letter for the company. The letter should be professional yet enthusiastic, highlighting how your skills align with the job requirements. It should be brief, straightforward, and feel personal—not overly polished or AI-generated. Use relevant keywords and maintain a pleasant and passionate tone. Include how I am a good fit for the role and keep it within 200 words.

Details:

        Job Description: {job_description}
        Company Name: {company_name}
        Structure:

        Introduction: Start by expressing genuine interest in the role and the company. Briefly mention your academic background.
        Relevant Experience: Highlight the most important aspects of your experience that directly align with the job description. Keep this natural and conversational, avoiding excessive detail.
        Company Fit: Briefly explain why the company's goals or mission resonate with you and how you see yourself contributing to the team.
        Closing: Conclude by expressing your enthusiasm for the role, your openness to further discussion in an interview, and appreciation for their time and consideration.
        Experience List: {experience_list}"""
        )

        chain_email = cover_letter_prompt | self.llm
        res = chain_email.invoke({"job_description": job_description,
        "company_name": company_name,
        "experience_list" : experience_list
        }
        )
        return res.content
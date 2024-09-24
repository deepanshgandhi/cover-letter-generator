company_points = {
    "Cognizant Technology Solutions" : 4,
    "Tata Consultancy Services" : 4,
    "Khoury College of Computer Sciences" : 3
}

job_detail_prompt = """
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

create_chromadb_query_prompt = """
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

generate_cover_letter_prompt = """Your name is Gibran Myageri, and you're a Software Engineer pursuing a Master's in Computer Science at Northeastern University. Based on the job description below, write a concise and tailored cover letter for the company. The letter should be professional yet enthusiastic, highlighting how your skills align with the job requirements. It should be brief, straightforward, and feel personal—not overly polished or AI-generated.

Details:
        Job Title: {job_title}
        Job Description: {job_description}
        Company Name: {company_name}
        Structure:

        Introduction: Start by expressing genuine interest in the role and the company. Briefly mention your academic background.
        Relevant Experience: Highlight the most important aspects of your experience which contains both professional experiences and your personal projects as well that directly align with the job description. Keep this natural and conversational, avoiding excessive detail.
        Company Fit: Briefly explain why the company's goals or mission resonate with you and how you see yourself contributing to the team.
        Closing: Conclude by expressing your enthusiasm for the role, your openness to further discussion in an interview, and appreciation for their time and consideration.
        Experience List: {experience_list}"""

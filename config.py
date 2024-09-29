company_points = {
    "Natwest Group" : 5,
    "Dunzo" : 0,
    "Standard Chartered Bank" : 3,
    "Webloom Solutions" : 3,
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

generate_cover_letter_prompt = """Your name is Deepansh Gandhi, a Machine Learning Intern at Staples while pursuing a Master’s in Artificial Intelligence at Northeastern University. Based on the job description below, write a concise and tailored cover letter for the company. The letter should be professional yet enthusiastic, highlighting how your skills align with the job requirements. Aim for a brief, straightforward tone that feels personal—not overly polished or AI-generated. Use relevant keywords and maintain a warm, passionate tone. Clearly illustrate why you are a good fit for the role.

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

generate_resume_points_prompt = """ 
                                    I am applying for the position of {job_title} at {company_name}. Below are the key responsibilities and qualifications mentioned in the job description. I have also provided a summary of my past experiences. Please review both and generate 3-5 bullet points for each experience that are most relevant to the job description. Make sure these points emphasize the key skills, technologies, and accomplishments related to the role.

                                    Job Description: {job_description}
                                    
                                    My past experiences : {experience_list}

                                    Instructions: Based on the job description and my experiences, generate concise bullet points under each experience that are tailored to match the responsibilities and qualifications of the job. Focus on the overlap between the skills and technologies mentioned in the job description and the work I’ve done in the past.

                                    Only use the information which is provided.
                                    Only return the valid JSON.
                                    It should not be a list. It should be a single JSON object.

                                    Return it in the following format:
                                    {{"experiences" : [
                                        {{
                                            "company": "Company Name 1",
                                            "job_description": ["Responsibility 1", "Responsibility 2", "Responsibility 3"],
                                            "job_title": "Job Title",
                                            "location": "Location"
                                        }},
                                        {{
                                            "company": "Company Name 2",
                                            "job_description": ["Responsibility 1", "Responsibility 2", "Responsibility 3"],
                                            "job_title": "Job Title",
                                            "location": "Location"
                                        }}
                                    ]}}
                                    ### VALID JSON (NO PREAMBLE):     
                                """
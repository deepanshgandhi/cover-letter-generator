import chromadb
import uuid
import json

class VectorDB:
    def __init__(self, chroma_client, collection_name):
        self.chroma_client = chromadb.PersistentClient(chroma_client)
        self.collection = self.chroma_client.get_or_create_collection(name=collection_name)

    def add_data(self, file_path):
        with open(file_path) as f:
            data = json.load(f)
        for job in data:
            for desc in job['responsibilities']:
                self.collection.add(
                    documents=[desc],
                    metadatas={
                        'company': job['company'],
                        'job_title': job['job_title'],
                    },
                    ids=[str(uuid.uuid4())]
                )

    def search(self, query, n_results=5):
        results = self.collection.query(query_texts=query, n_results=n_results)
        documents = results['documents'][0]
        metadata = results['metadatas'][0]
        job_experience = []
        for i in range(len(documents)):
            job_experience.append({'company': metadata[i]['company'], 'job_description': documents[i]})
        merged_jobs = {}
        for job in job_experience:
            company = job['company']
            job_desc = job['job_description']
            
            if company in merged_jobs:
                merged_jobs[company] += ', ' + job_desc
            else:
                merged_jobs[company] = job_desc
        merged_jobs_list = [{'company': company, 'job_description': description} for company, description in merged_jobs.items()]
        return merged_jobs_list
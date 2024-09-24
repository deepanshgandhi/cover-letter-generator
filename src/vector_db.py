import chromadb
import uuid
import json

class VectorDB:
    def __init__(self, chroma_client, collection_name):
        self.chroma_client = chromadb.PersistentClient(chroma_client)
        """try:
            self.collection = self.chroma_client.get_collection(name=collection_name)
            self.chroma_client.delete_collection(name=collection_name)
        except:
            pass
        """
        self.collection = self.chroma_client.get_or_create_collection(name=collection_name)

    def add_data(self, file_path):
        with open(file_path) as f:
            data = json.load(f)
        for job in data:
            for desc in job['responsibilities']:
                print(desc)
                self.collection.add(
                    documents=[desc],
                    metadatas={
                        'company': job['company'],
                        'job_title': job['job_title'],
                        'project': job['project'],
                        'location': job['location']
                    },
                    ids=[str(uuid.uuid4())]
                )

    def merge_data(self, search_results):
        merged_data = {}
        for result in search_results:
            company = result['company']
            job_desc = result['job_description']
            job_title = result['job_title']
            location = result['location']
            project = result['project']

            if company == "":
                # That means its a project
                if job_title not in merged_data:
                    merged_data[job_title] = {}
                    merged_data[job_title]["job_description"] = job_desc
                    merged_data[job_title]["project"] = project
                    merged_data[job_title]["location"] = location
                    merged_data[job_title]["job_title"] = job_title
                else:
                    merged_data[job_title]["job_description"] += ', ' + job_desc
                
            else:
                if company in merged_data:
                    merged_data[company]["job_description"] += ', ' + job_desc
                    
                else:
                    merged_data[company] = {}
                    merged_data[company]["job_description"] = job_desc
                    merged_data[company]["location"] = location
                    merged_data[company]["project"] = project
                    merged_data[company]["job_title"] = job_title

        merged_data_list = []

        for key in merged_data:
            if merged_data[key]["project"] != "":
                merged_data_list.append({
                    'company': "",
                    'job_description': merged_data[key]["job_description"],
                    'job_title': "",
                    'project': merged_data[key]["project"],
                    'location': merged_data[key]["location"]
                })
            else:
                merged_data_list.append({
                    'company': key,
                    'job_description': merged_data[key]["job_description"],
                    'job_title': merged_data[key]["job_title"],
                    'project': "",
                    'location': merged_data[key]["location"]
                })
        return merged_data_list
        



    def search(self, query, n_results=10):
        results = self.collection.query(query_texts=query, n_results=n_results)
        documents = results['documents'][0]
        metadata = results['metadatas'][0]
        job_experience = []
        for i in range(len(documents)):
            job_experience.append({
                'company': metadata[i]['company'],
                'job_description': documents[i],
                'job_title': metadata[i]['job_title'],
                'project': metadata[i]['project'],
                'location': metadata[i]['location']
                })
        merged_jobs = {}
        merged_jobs_list = self.merge_data(job_experience)
        # for job in job_experience:
        #     company = job['company']
        #     job_desc = job['job_description']
            
        #     if company in merged_jobs:
        #         merged_jobs[company] += ', ' + job_desc
        #     else:
        #         merged_jobs[company] = job_desc
                
        # merged_jobs_list = [{'company': company, 'job_description': description, 'job_title': job_title, 'project': project} for company, description, job_title, project in merged_jobs.items()]
        return merged_jobs_list
    
    def search_by_company(self, query, company_name, n_results=2):
        results = self.collection.query(
            query_texts=query,
            where={'company': company_name},
            n_results=n_results
        )
        return results['documents'][0]


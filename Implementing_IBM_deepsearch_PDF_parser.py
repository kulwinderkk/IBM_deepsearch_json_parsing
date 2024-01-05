#####
# Using IBM DeepSearch to parse the PDF files to JSON
# Need to have account on IBM Deepsearch
# do pip install deepsearch-toolkit
# set up profile using the toolkit user login and api key
####


import os
from deepsearch.cps.client.api import CpsApi
import deepsearch as ds
import zipfile
import json
from dotenv import load_dotenv

def docs_to_json(path_to_docs: str, save_json:bool, result_dir:str) -> list[dict]:
    

    for file in os.listdir(path_to_docs):
        filepath=os.path.join(os.path.abspath(path_to_docs), file)
        documents = ds.convert_documents(api=deepsearch_api_key,proj_key=deepsearch_project_key, source_path=filepath)
        documents.download_all(result_dir = result_dir)

         for document in os.listdir(result_dir):
            if document.endswith(".zip"):
                print(document)
                with zipfile.ZipFile(os.path.join(result_dir, document), 'r') as z:
                    for filename in z.namelist():
                        if filename.endswith(".json"):
                            print(filename)
                            with z.open(filename) as f:
                                data = json.loads(f.read().decode("utf-8"))
                                if save_json:
                                    with open(os.path.join(result_dir, filename), "w") as f:
                                        json.dump(data, f, indent=4)

if __name__ == "__main__":

    load_dotenv()
    result_dir = "./results/"
    save_json = True
    document_folder='./docs'
    # you need to get an api key and configure your profile before.
    deepsearch_api_key = CpsApi.from_env()

    # assumes that you only have one project, otherwise you need to specify the project key
    deepsearch_project_key = api.projects.list()[0].key
    path_to_docs = document_folder

    documents = docs_to_json(path_to_docs=path_to_docs, save_json=save_json, result_dir=result_dir)
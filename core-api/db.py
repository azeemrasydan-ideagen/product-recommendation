import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from config import hf_api_key

def get_ideagen_products_db():
    embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=hf_api_key, model_name="sentence-transformers/all-MiniLM-l6-v2"
)
    current_dir = os.getcwd()
    db_dir = os.path.join(current_dir, "db")
    persistent_directory = os.path.join(db_dir, "ideagen_products_db")
    db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)
    return db

db = get_ideagen_products_db()
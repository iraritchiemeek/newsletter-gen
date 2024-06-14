import os
import voyageai
from sqlmodel import Session
from models import Embedding
from db import engine

from summariser import get_json_summaries

vo = voyageai.Client()
data_dir = "./data"

def save_embedding(embedding, file_name):
    embedding = Embedding(
        meta={
            "file_name": file_name
        },
        embedding=embedding
    )
    with Session(engine) as session:
        session.add(embedding)
        session.commit()

def get_embedding_from_summaries(summaries):
    texts = [f"{title}: {summary}" for title, summary in summaries.items()]
    embeddings = vo.embed(texts, model="voyage-large-2-instruct")
    return embeddings

def load_txt_file(file_path):
    with open(file_path, "r") as file:
        return file.read()
    
def load_all_txt_files():
    for file in os.listdir(data_dir):
        if file.endswith(".txt"):
            yield file, load_txt_file(os.path.join(data_dir, file))

if __name__ == "__main__":
    for file_name, file_content in load_all_txt_files():
        json_summaries = get_json_summaries(file_content)
        embeddings = get_embedding_from_summaries(json_summaries)
        for embedding in embeddings.embeddings:
            save_embedding(embedding, file_name)
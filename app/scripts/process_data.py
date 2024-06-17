import os
from semantic_router.encoders import OpenAIEncoder
from semantic_chunkers import StatisticalChunker

from create_embeddings import get_chunk_embeddings, save_embedding

encoder = OpenAIEncoder(name="text-embedding-3-small")
chunker = StatisticalChunker(encoder=encoder)

DATA_DIR = "./data"

def get_chunks(text):
    chunks = chunker(docs=[text])
    return chunks[0]

def load_txt_file(file_path):
    with open(file_path, "r") as file:
        return file.read()
    
def load_all_txt_files():
    for file in os.listdir(DATA_DIR):
        if file.endswith(".txt"):
            yield file, load_txt_file(os.path.join(DATA_DIR, file))

if __name__ == "__main__":
    for file_name, file_content in load_all_txt_files():
        chunks = get_chunks(file_content)
        embeddings = get_chunk_embeddings(chunks)
        if len(embeddings) != len(chunks):
            print(f"Number of embeddings does not match number of chunks for {file_name}")
            continue
        for i in range(len(chunks)):
            save_embedding(embeddings[i], chunks[i], file_name)

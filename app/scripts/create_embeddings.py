import os
import voyageai
from sqlmodel import Session
from models import Embedding, Chunk
from db import engine

vo = voyageai.Client()

def has_similar_embedding(embedding):
    from sqlmodel import select
    from models import Embedding

    with Session(engine) as session:
        result = session.exec(
            select(Embedding.embedding.l2_distance(embedding)).order_by(Embedding.embedding.l2_distance(embedding)).limit(1)
        )
    return result.first()

def chunk_splits_to_text(chunk):
    print(chunk)
    return " ".join(chunk.splits)

def save_embedding(embedding, chunk, file_name):
    chunk = Chunk(
        text=chunk_splits_to_text(chunk),
        meta={
            "file_name": file_name
        }
    )
    embedding = Embedding(
        embedding=embedding,
        chunk=chunk
    )
    with Session(engine) as session:
        session.add(chunk)
        session.add(embedding)
        session.commit()

def get_chunk_embeddings(chunks):
    texts = [chunk_splits_to_text(chunk) for chunk in chunks]
    result = vo.embed(texts, model="voyage-large-2-instruct")
    return result.embeddings


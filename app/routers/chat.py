from fastapi import APIRouter
from sqlmodel import select
from models import Embedding
from openai import OpenAI
from sqlmodel import Session
from db import engine
import voyageai

vo = voyageai.Client()
client = OpenAI()

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)

MODEL = 'gpt-4o'

def get_context(message: str):
    context = {}
    embedding = vo.embed(message, model="voyage-large-2-instruct").embeddings[0]
    with Session(engine) as session:
        results = session.exec(
            select(Embedding).order_by(Embedding.embedding.l2_distance(embedding)).limit(5)
        )
        for i, result in enumerate(results, start=1):
            context[f"context_{i}"] = result.chunk.text
    return context

def create_completion(message: str):
    context = get_context(message)
    PROMPT = f"""
    You are an expert copy writer. 
    Your task is to write a paragraph based on the user's prompt in the style of the context.
    #IMPORTANT# 
    - Your response should match the tone and style of the contexts averaged.
    - Your response should match the length of the context averaged.
    - Your response should be relevant to the prompt.
    - Do not include links or newlines.
    Context: {context}
    Prompt: {message}
    """
    print(PROMPT)
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": message}
        ]
    )
    return completion

# def create_completion(message: str):
#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a friendly chat bot."},
#             {"role": "user", "content": message}
#         ]
#     )
#     return completion.choices[0].message

@router.get("/")
async def create_response(message: str):
    # return {"message": get_context(message)}
    return {"message": create_completion(message)}

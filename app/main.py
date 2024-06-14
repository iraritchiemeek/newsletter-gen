from fastapi import FastAPI

from routers import embeddings

app = FastAPI()

app.include_router(embeddings.router)

@app.get("/")
async def root():
    return {"Hello World"}
from pgvector.sqlalchemy import Vector
from sqlmodel import Field, SQLModel, Column, JSON, Relationship
from typing import Optional, Any
from datetime import datetime

class Chunk(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  text: str = Field()
  meta: dict = Field(sa_column=Column(JSON))
  embeddings: list["Embedding"] = Relationship(back_populates="chunk")
  created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
  updated_at: datetime = Field(default=datetime.utcnow(), nullable=False)

class Embedding(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  embedding: Any = Field(sa_column=Column(Vector(1024)))
  chunk_id: int = Field(default=None, foreign_key="chunk.id")
  chunk: Chunk = Relationship(back_populates="embeddings")
  created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
  updated_at: datetime = Field(default=datetime.utcnow(), nullable=False)
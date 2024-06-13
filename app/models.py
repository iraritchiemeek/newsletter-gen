from pgvector.sqlalchemy import Vector
from sqlmodel import Field, SQLModel, Column, JSON
from typing import Optional, Any
from datetime import datetime

class Embedding(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  embedding: Any = Field(sa_column=Column(Vector(1024)))
  meta: dict = Field(sa_column=Column(JSON))
  created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
  updated_at: datetime = Field(default=datetime.utcnow(), nullable=False)
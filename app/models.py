from pgvector.sqlalchemy import Vector
from sqlmodel import Field, SQLModel
from typing import Optional

class Embedding(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

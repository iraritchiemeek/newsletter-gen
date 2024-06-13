import os
from sqlmodel import SQLModel, create_engine, Session, text
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}"
SERVER_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost/postgres"

def create_db_and_add_extension():
    server_engine = create_engine(SERVER_URL, isolation_level="AUTOCOMMIT", echo=True)
    with server_engine.connect() as connection:
        result = connection.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'"))
        if not result.scalar():
            connection.execute(text(f'CREATE DATABASE {DB_NAME}'))
        result.close()

    engine = create_engine(DATABASE_URL, echo=True)
    with Session(engine) as session:
        session.exec(text('CREATE EXTENSION IF NOT EXISTS vector'))
        session.commit()
    SQLModel.metadata.create_all(engine)

create_db_and_add_extension()
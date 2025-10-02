# backend/db.py
from sqlmodel import SQLModel, create_engine, Session

DB_FILE = "eldercare.db"
engine = create_engine(f"sqlite:///{DB_FILE}", echo=False)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

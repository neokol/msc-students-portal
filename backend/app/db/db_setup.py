import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
print(DB_URL)
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:#Po$tGReSQL#7915@localhost:5432/AcademicPortal"

engine = create_engine(
    DB_URL, connect_args={}, future=True
)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)

Base = declarative_base()

# DB Utilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
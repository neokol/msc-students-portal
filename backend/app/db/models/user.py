from sqlalchemy import Column, Integer, String

from app.db.db_setup import Base



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), unique=True, index=True)
    full_name = Column(String(256))
    email = Column(String(256))
    hashed_password = Column(String(256))
    role = Column(String(256))

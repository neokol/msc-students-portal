from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship


from app.db.db_setup import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    teacher = relationship("User")
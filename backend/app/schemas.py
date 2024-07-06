from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    role: str
    full_name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    name: str

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

    class Config:
        orm_mode = True

class GradeBase(BaseModel):
    student_id: int
    course_id: int
    grade: float

class GradeCreate(GradeBase):
    pass

class Grade(GradeBase):
    id: int
    is_finalized: bool

    class Config:
        orm_mode = True


class GradeWithCourse(BaseModel):
    id: int
    student_id: int
    course_id: int
    grade: float | None
    course_name: str

    class Config:
        orm_mode = True
        
class CourseWithStudents(BaseModel):
    course_id: int
    course_name: str | None
    student_id: int
    student_name: str | None
    grade_id: int
    grade: Optional[float] | None

    class Config:
        orm_mode = True

class CourseWithGradesAndStudents(BaseModel):
    course_id: int
    course_name: str | None
    student_id: int
    student_name: str | None
    grade: Optional[float] | None
    grade_id: int | None
    is_finalized: Optional[bool] | None

    class Config:
        orm_mode = True

class GradeUpdate(BaseModel):
    grade: float | None

    class Config:
        orm_mode = True
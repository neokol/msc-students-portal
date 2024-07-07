from fastapi import HTTPException, Depends, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session 
from sqlalchemy.sql import select, join
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

from app.db.models.user import User
from app.db.models.course import Course
from app.db.models.grade import Grade
from app.schemas import UserCreate, CourseCreate, GradeCreate
from app.db.db_setup import get_db

load_dotenv() 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SECRET_KEY = "your_secret_key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 300


my_secret_key = os.getenv('SECRET_KEY')
my_algorithm = os.getenv('ALGORITHM')
token_expire = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password, role=user.role, full_name = user.full_name, email = user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_course(db: Session, course: CourseCreate):
    db_course = Course(name = course.name )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


# Authenticate the user
def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

# Create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, my_secret_key, algorithm=my_algorithm)
    return encoded_jwt

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, my_secret_key, algorithms=[my_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Token is invalid or expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Token is invalid or expired")

def get_user_id_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, my_secret_key, algorithms=[my_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == username).first()
    if user is None:
        raise credentials_exception
    return user.id





def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Course).offset(skip).limit(limit).all()


# def create_grade(db: Session, grade: GradeCreate):
#     db_grade = Grade()
#     db.add(db_grade)
#     db.commit()
#     db.refresh(db_grade)
#     return db_grade

def get_grades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Grade).offset(skip).limit(limit).all()


def get_student_courses(db: Session, student_id: int):
    stmt = (
        select(
            Grade.id,
            Grade.student_id,
            Grade.course_id,
            Grade.grade,
            Course.name.label('course_name')
        )
        .select_from(
            join(Grade, Course, Grade.course_id == Course.id)
        )
        .where(Grade.student_id == student_id)
    )
    result = db.execute(stmt).all()
    return result


def get_teacher_courses_with_students(db: Session, teacher_id: int):
    stmt = (
        select(
            Course.id.label("course_id"),
            Course.name.label("course_name"),
            User.id.label("student_id"),
            User.full_name.label("student_name"),
            Grade.id.label("grade_id"),
            Grade.grade
        )
        .select_from(
            join(Course, Grade, Course.id == Grade.course_id)
            .join(User, Grade.student_id == User.id)
        )
        .where(Course.teacher_id == teacher_id)
    )
    result = db.execute(stmt).all()
    return result


def get_all_courses_with_grades_and_students(db: Session):
    stmt = (
        select(
            Course.id.label("course_id"),
            Course.name.label("course_name"),
            User.id.label("student_id"),
            User.full_name.label("student_name"),
            Grade.id.label("grade_id"),
            Grade.grade,
            Grade.is_finalized
        )
        .select_from(
            join(Course, Grade, Course.id == Grade.course_id)
            .join(User, Grade.student_id == User.id)
        )
    )
    result = db.execute(stmt).all()
    return result



def update_grade(db: Session, grade_id: int, grade: float):
    db_grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if db_grade:
        db_grade.grade = grade
        db.commit()
        db.refresh(db_grade)
        return db_grade
    return None


def finalize_grade(db: Session, grade_id: int):
    db_grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if db_grade:
        db_grade.is_finalized = True
        db.commit()
        db.refresh(db_grade)
        return db_grade
    return None
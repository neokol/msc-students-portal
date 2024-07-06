import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import get_courses, create_course
from app.db.db_setup import get_db
from app.schemas import CourseCreate,Course

router= fastapi.APIRouter()


@router.get("/courses/", response_model=list[Course], tags=["Courses"])
async def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = get_courses(db)
    return courses

@router.post("/course/",  tags=["Courses"])
async def create_new_course(course: CourseCreate, db: Session = Depends(get_db)):
    return create_course(db=db, course=course)




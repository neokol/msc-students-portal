from typing import List
import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import finalize_grade, get_all_courses_with_grades_and_students, get_grades, get_student_courses, get_teacher_courses_with_students, update_grade
from app.db.db_setup import get_db
from app.schemas import Course, CourseWithGradesAndStudents, CourseWithStudents, Grade,GradeCreate, GradeUpdate, GradeWithCourse
from app.dependencies import get_current_user_id
from app.email_service import send_email
from app.db.models.user import User
from app.db.models.course import Course

router= fastapi.APIRouter()


@router.get("/grades/", response_model=list[Grade], tags=["Grades"])
async def read_grades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    grades = get_grades(db)
    return grades

# @router.post("/grade/")
# async def create_new_course(grade: GradeCreate, db: Session = Depends(get_db)):
#     return create_grade(db=db, grade=grade)


# @router.get("/students/{student_id}/courses", response_model=List[GradeWithCourse], tags=["Courses"])
# def read_student_courses(student_id: int, db: Session = Depends(get_db)):
#     courses = get_student_courses(db, student_id=student_id)
#     if not courses:
#         raise HTTPException(status_code=404, detail="Student not found or no courses available")
#     return courses

@router.get("/students/{student_id}/courses", response_model=List[GradeWithCourse])
def read_student_courses(student_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    if student_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this data")
    courses = get_student_courses(db, student_id=student_id)
    if not courses:
        raise HTTPException(status_code=404, detail="Student not found or no courses available")
    return courses


@router.get("/teachers/{teacher_id}/courses", response_model=List[CourseWithStudents], tags=["Courses"])
def read_teacher_courses(teacher_id: int, db: Session = Depends(get_db)):
    courses = get_teacher_courses_with_students(db, teacher_id=teacher_id)
    if not courses:
        raise HTTPException(status_code=404, detail="Teacher not found or no courses available")
    return courses


@router.get("/helpdesk/courses", response_model=List[CourseWithGradesAndStudents])
def read_all_courses_with_grades_and_students(db: Session = Depends(get_db)):
    courses = get_all_courses_with_grades_and_students(db)
    if not courses:
        raise HTTPException(status_code=404, detail="No courses available")
    return courses



@router.put("/grades/{grade_id}", response_model=GradeUpdate)
def update_student_grade(grade_id: int, grade: GradeUpdate, db: Session = Depends(get_db)):
    updated_grade = update_grade(db, grade_id=grade_id, grade=grade.grade)
    if not updated_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return updated_grade


@router.put("/grades/{grade_id}/finalize", response_model=Grade)
def finalize_student_grade(grade_id: int, db: Session = Depends(get_db)):
    updated_grade = finalize_grade(db, grade_id=grade_id)
    if not updated_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    
    
    # Fetch the student and course details to send the email
    student = db.query(User).filter(User.id == updated_grade.student_id).first()
    course_info = db.query(Course).filter(Course.id == updated_grade.course_id).first()
    print(student.email)
    print(course_info.name)
    print(updated_grade.grade)
    if student and course_info:
        send_email(email=student.email, lesson_title=course_info.name, grade=updated_grade.grade)
    return updated_grade
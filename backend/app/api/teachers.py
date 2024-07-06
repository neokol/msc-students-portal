# import fastapi

# router= fastapi.APIRouter()

# @router.post("/grades/", response_model=schemas.Grade)
# def create_grade(grade: schemas.GradeCreate, db: Session = Depends(database.SessionLocal), current_user: schemas.User = Depends(auth.get_current_active_user)):
#     if current_user.role != "professor":
#         raise HTTPException(status_code=403, detail="Not enough permissions")
#     return crud.create_grade(db, grade=grade)
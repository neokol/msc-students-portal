# import fastapi

# router= fastapi.APIRouter()

# @router.put("/grades/{grade_id}/finalize", response_model=schemas.Grade)
# def finalize_grade(grade_id: int, db: Session = Depends(database.SessionLocal), current_user: schemas.User = Depends(auth.get_current_active_user)):
#     if current_user.role != "secretary":
#         raise fastapi.HTTPException(status_code=403, detail="Not enough permissions")
#     return 1
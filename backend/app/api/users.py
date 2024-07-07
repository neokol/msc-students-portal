import fastapi
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
from dotenv import load_dotenv

from app.crud import authenticate_user, create_access_token, get_user, create_user, get_users, verify_token
from app.db.db_setup import get_db
from app.schemas import UserCreate,User
load_dotenv() 



my_secret_key = os.getenv('SECRET_KEY')
my_algorithm = os.getenv('ALGORITHM')
token_expire = 300

router= fastapi.APIRouter()

# @router.get("/user_grades/", response_model=List[Grade])
# def read_grades(skip: int = 0, limit: int = 10, db: Session = Depends(database.SessionLocal), current_user: User = Depends(auth.get_current_active_user)):
#     return crud.get_grades(db, student_id=current_user.id)




@router.get("/users/", response_model=list[User],  tags=["Users"])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db)
    return users

@router.post("/users",  tags=["Users"])
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)



@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=token_expire)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify-token/{token}")
async def verify_user_token(token: str):
    verify_token(token=token)
    return {"message": "Token is valid"}
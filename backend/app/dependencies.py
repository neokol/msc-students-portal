from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.db_setup import get_db
from app.crud import get_user_id_from_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user_id(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return get_user_id_from_token(token, db)

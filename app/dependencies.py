from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer 
from jose import JWTError, jwt 
from sqlalchemy.orm import Session 
from app.core.config import SECRET_KEY, ALGORITHM 
from app.database import SessionLocal 
from app.repositories import user as user_repo 

oauth2_scheme=OAuth2PasswordBearer (tokenUrl="token")

def get_db ():
    db=SessionLocal ()
    try:
        yield db 
    finally:
        db.close ()

async def get_current_user (token: str=Depends (oauth2_scheme), db: Session=Depends (get_db)):
    credentials_exception=HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}, )
    try:
        payload=jwt.decode (token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str=payload.get ("sub")
        if username is None:
            raise credentials_exception 
    except JWTError:
        raise credentials_exception 
    user=user_repo.get_user_by_username (db, username=username)
    if user is None:
        raise credentials_exception 
    return user 

async def get_current_active_user (current_user=Depends (get_current_user)):
    return current_user 

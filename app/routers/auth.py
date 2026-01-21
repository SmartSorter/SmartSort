from datetime import timedelta 
from fastapi import APIRouter, Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session 

from app.database import SessionLocal 
from app.core import security 
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES 
from app.repositories import user as user_repo 

router=APIRouter (tags=["authentication"])

def get_db ():
    db=SessionLocal ()
    try:
        yield db 
    finally:
        db.close ()

@router.post ("/token")
async def login_for_access_token (form_data: OAuth2PasswordRequestForm=Depends (), db: Session=Depends (get_db)):
    user=user_repo.get_user_by_username (db, username=form_data.username)
    if not user or not security.verify_password (form_data.password, user.hashed_password):
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}, )
    access_token_expires=timedelta (minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token=security.create_access_token (data={"sub": user.username, "role": user.role }, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

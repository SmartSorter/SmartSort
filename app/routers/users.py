from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
from typing import List 

from app.database import SessionLocal 
from app.schemas.user import UserCreate, UserResponse 
from app.repositories import user as user_repo 

router=APIRouter (prefix="/users",
tags=["users"])

def get_db ():
    db=SessionLocal ()
    try:
        yield db 
    finally:
        db.close ()

@router.post ("/", response_model=UserResponse)
def create_user (user: UserCreate, db: Session=Depends (get_db)):
    db_user=user_repo.get_user_by_username (db, username=user.username)
    if db_user:
        raise HTTPException (status_code=400, detail="Username already registered")
    return user_repo.create_user (db=db, user=user)

from app.dependencies import get_current_active_user 
from app.schemas.user import UserResponse 

@router.get ("/", response_model=List [UserResponse])
def read_users (skip: int=0, limit: int=100, db: Session=Depends (get_db), current_user=Depends (get_current_active_user)):
    users=user_repo.get_users (db, skip=skip, limit=limit)
    return users 

@router.get ("/{user_id}", response_model=UserResponse)
def read_user (user_id: int, db: Session=Depends (get_db)):
    db_user=user_repo.get_user (db, user_id=user_id)
    if db_user is None:
        raise HTTPException (status_code=404, detail="User not found")
    return db_user 

from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
from typing import List 

from app.database import SessionLocal 
from app.schemas.waste_type import WasteTypeCreate, WasteTypeResponse 
from app.repositories import waste_type as waste_type_repo 

router=APIRouter (prefix="/waste-types",
tags=["waste-types"])

def get_db ():
    db=SessionLocal ()
    try:
        yield db 
    finally:
        db.close ()

@router.post ("/", response_model=WasteTypeResponse)
def create_waste_type (waste_type: WasteTypeCreate, db: Session=Depends (get_db)):
    return waste_type_repo.create_waste_type (db=db, waste_type=waste_type)

@router.get ("/", response_model=List [WasteTypeResponse])
def read_waste_types (skip: int=0, limit: int=100, db: Session=Depends (get_db)):
    waste_types=waste_type_repo.get_waste_types (db, skip=skip, limit=limit)
    return waste_types 

@router.get ("/{waste_type_id}", response_model=WasteTypeResponse)
def read_waste_type (waste_type_id: int, db: Session=Depends (get_db)):
    db_waste_type=waste_type_repo.get_waste_type (db, waste_type_id=waste_type_id)
    if db_waste_type is None:
        raise HTTPException (status_code=404, detail="Waste type not found")
    return db_waste_type 

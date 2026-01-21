from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
from typing import List 

from app.database import SessionLocal 
from app.schemas.container import ContainerCreate, ContainerResponse, ContainerUpdate 
from app.repositories import container as container_repo 

router=APIRouter (prefix="/containers",
tags=["containers"])

def get_db ():
    db=SessionLocal ()
    try:
        yield db 
    finally:
        db.close ()

@router.post ("/", response_model=ContainerResponse)
def create_container (container: ContainerCreate, db: Session=Depends (get_db)):
    return container_repo.create_container (db=db, container=container)

@router.get ("/", response_model=List [ContainerResponse])
def read_containers (skip: int=0, limit: int=100, db: Session=Depends (get_db)):
    containers=container_repo.get_containers (db, skip=skip, limit=limit)
    return containers 

@router.get ("/{container_id}", response_model=ContainerResponse)
def read_container (container_id: int, db: Session=Depends (get_db)):
    db_container=container_repo.get_container (db, container_id=container_id)
    if db_container is None:
        raise HTTPException (status_code=404, detail="Container not found")
    return db_container 

@router.patch ("/{container_id}/fill-level", response_model=ContainerResponse)
def update_container_fill_level (container_id: int, fill_level_data: ContainerUpdate, db: Session=Depends (get_db)):
    db_container=container_repo.update_container_fill_level (db, container_id=container_id, fill_level=fill_level_data.fill_level)
    if db_container is None:
        raise HTTPException (status_code=404, detail="Container not found")
    return db_container 

from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
from typing import List 

from app.database import SessionLocal 
from app.schemas.route import RouteCreate, RouteResponse 
from app.repositories import route as route_repo 

router=APIRouter (prefix="/routes",
tags=["routes"])

def get_db ():
    db=SessionLocal ()
    try:
        yield db 
    finally:
        db.close ()

from app.services import waste_service 

@router.post ("/", response_model=RouteResponse)
def create_route (route: RouteCreate, db: Session=Depends (get_db)):
    return route_repo.create_route (db=db, route=route)

@router.post ("/optimize", response_model=RouteResponse)
def create_optimized_route (db: Session=Depends (get_db)):
    description=waste_service.generate_optimization_route (db)
    route_create=RouteCreate (description=description)
    return route_repo.create_route (db=db, route=route_create)

@router.get ("/", response_model=List [RouteResponse])
def read_routes (skip: int=0, limit: int=100, db: Session=Depends (get_db)):
    routes=route_repo.get_routes (db, skip=skip, limit=limit)
    return routes 

@router.get ("/{route_id}", response_model=RouteResponse)
def read_route (route_id: int, db: Session=Depends (get_db)):
    db_route=route_repo.get_route (db, route_id=route_id)
    if db_route is None:
        raise HTTPException (status_code=404, detail="Route not found")
    return db_route 

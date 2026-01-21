from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
from typing import List 

from app.database import SessionLocal 
from app.schemas.alert import AlertCreate, AlertResponse 
from app.repositories import alert as alert_repo 

router=APIRouter (prefix="/alerts",
tags=["alerts"])

def get_db ():
    db=SessionLocal ()
    try:
        yield db 
    finally:
        db.close ()

@router.post ("/", response_model=AlertResponse)
def create_alert (alert: AlertCreate, db: Session=Depends (get_db)):
    return alert_repo.create_alert (db=db, alert=alert)

@router.get ("/", response_model=List [AlertResponse])
def read_alerts (skip: int=0, limit: int=100, db: Session=Depends (get_db)):
    alerts=alert_repo.get_alerts (db, skip=skip, limit=limit)
    return alerts 

@router.get ("/{alert_id}", response_model=AlertResponse)
def read_alert (alert_id: int, db: Session=Depends (get_db)):
    db_alert=alert_repo.get_alert (db, alert_id=alert_id)
    if db_alert is None:
        raise HTTPException (status_code=404, detail="Alert not found")
    return db_alert 

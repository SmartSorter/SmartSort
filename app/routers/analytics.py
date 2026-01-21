from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session 
from app.database import SessionLocal 
from app.services import analytics_service 

router=APIRouter (prefix="/analytics",
tags=["analytics"])

def get_db ():
    db=SessionLocal ()
    try:
        yield db 
    finally:
        db.close ()

@router.get ("/waste-stats")
def get_waste_statistics (db: Session=Depends (get_db)):
    return analytics_service.get_waste_stats (db)

@router.post ("/check-health")
def trigger_health_check (db: Session=Depends (get_db)):
    alerts=analytics_service.check_device_health (db)
    return {"status": "Health check complete", "alerts_generated": len (alerts)}

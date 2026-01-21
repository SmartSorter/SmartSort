from sqlalchemy.orm import Session 
from app.models.alert import Alert 
from app.schemas.alert import AlertCreate 

def get_alert (db: Session, alert_id: int):
    return db.query (Alert).filter (Alert.id==alert_id).first ()

def get_alerts (db: Session, skip: int=0, limit: int=100):
    return db.query (Alert).offset (skip).limit (limit).all ()

def create_alert (db: Session, alert: AlertCreate):
    db_alert=Alert (container_id=alert.container_id, message=alert.message)
    db.add (db_alert)
    db.commit ()
    db.refresh (db_alert)
    return db_alert 

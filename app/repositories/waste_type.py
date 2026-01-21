from sqlalchemy.orm import Session 
from app.models.waste_type import WasteType 
from app.schemas.waste_type import WasteTypeCreate 

def get_waste_type (db: Session, waste_type_id: int):
    return db.query (WasteType).filter (WasteType.id==waste_type_id).first ()

def get_waste_types (db: Session, skip: int=0, limit: int=100):
    return db.query (WasteType).offset (skip).limit (limit).all ()

def create_waste_type (db: Session, waste_type: WasteTypeCreate):
    db_waste_type=WasteType (name=waste_type.name)
    db.add (db_waste_type)
    db.commit ()
    db.refresh (db_waste_type)
    return db_waste_type 

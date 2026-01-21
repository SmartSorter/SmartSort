from sqlalchemy.orm import Session 
from app.models.device import Device 
from app.schemas.device import DeviceCreate, DeviceUpdate 

def get_device (db: Session, device_id: int):
    return db.query (Device).filter (Device.id==device_id).first ()

def get_device_by_serial (db: Session, serial_number: str):
    return db.query (Device).filter (Device.serial_number==serial_number).first ()

def get_devices (db: Session, skip: int=0, limit: int=100):
    return db.query (Device).offset (skip).limit (limit).all ()

def create_device (db: Session, device: DeviceCreate):
    db_device=Device (serial_number=device.serial_number,
    location=device.location,
    is_active=device.is_active)
    db.add (db_device)
    db.commit ()
    db.refresh (db_device)
    return db_device 

def update_device (db: Session, device_id: int, device_update: DeviceUpdate):
    db_device=get_device (db, device_id)
    if not db_device:
        return None 

    update_data=device_update.dict (exclude_unset=True)
    for key, value in update_data.items ():
        setattr (db_device, key, value)

    db.add (db_device)
    db.commit ()
    db.refresh (db_device)
    return db_device 

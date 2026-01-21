from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
from typing import List 

from app.database import SessionLocal 
from app.schemas.device import DeviceCreate, DeviceResponse, DeviceUpdate 
from app.repositories import device as device_repo 

router=APIRouter (prefix="/devices",
tags=["devices"])

def get_db ():
    db=SessionLocal ()
    try:
        yield db 
    finally:
        db.close ()

@router.post ("/", response_model=DeviceResponse)
def create_device (device: DeviceCreate, db: Session=Depends (get_db)):
    db_device=device_repo.get_device_by_serial (db, serial_number=device.serial_number)
    if db_device:
        raise HTTPException (status_code=400, detail="Device with this serial number already exists")
    return device_repo.create_device (db=db, device=device)

@router.get ("/", response_model=List [DeviceResponse])
def read_devices (skip: int=0, limit: int=100, db: Session=Depends (get_db)):
    devices=device_repo.get_devices (db, skip=skip, limit=limit)
    return devices 

@router.get ("/{device_id}", response_model=DeviceResponse)
def read_device (device_id: int, db: Session=Depends (get_db)):
    db_device=device_repo.get_device (db, device_id=device_id)
    if db_device is None:
        raise HTTPException (status_code=404, detail="Device not found")
    return db_device 

@router.patch ("/{device_id}", response_model=DeviceResponse)
def update_device (device_id: int, device_update: DeviceUpdate, db: Session=Depends (get_db)):
    db_device=device_repo.update_device (db, device_id=device_id, device_update=device_update)
    if db_device is None:
        raise HTTPException (status_code=404, detail="Device not found")
    return db_device 

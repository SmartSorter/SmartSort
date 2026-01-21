from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
from typing import List 

from app.database import SessionLocal 
from app.schemas.sensor_data import SensorDataCreate, SensorDataResponse 
from app.repositories import sensor_data as sensor_data_repo 

router=APIRouter (prefix="/sensor-data",
tags=["sensor-data"])

def get_db ():
    db=SessionLocal ()
    try:
        yield db 
    finally:
        db.close ()

from app.services import waste_service 

@router.post ("/", response_model=SensorDataResponse)
def create_sensor_data (sensor_data: SensorDataCreate, db: Session=Depends (get_db)):

    new_data=sensor_data_repo.create_sensor_data (db=db, sensor_data=sensor_data)


    waste_service.check_fill_level (db=db, container_id=sensor_data.container_id, fill_level=sensor_data.fill_level)

    return new_data 

@router.get ("/", response_model=List [SensorDataResponse])
def read_all_sensor_data (skip: int=0, limit: int=100, db: Session=Depends (get_db)):
    all_sensor_data=sensor_data_repo.get_all_sensor_data (db, skip=skip, limit=limit)
    return all_sensor_data 

@router.get ("/{sensor_data_id}", response_model=SensorDataResponse)
def read_sensor_data (sensor_data_id: int, db: Session=Depends (get_db)):
    db_sensor_data=sensor_data_repo.get_sensor_data (db, sensor_data_id=sensor_data_id)
    if db_sensor_data is None:
        raise HTTPException (status_code=404, detail="Sensor data not found")
    return db_sensor_data 

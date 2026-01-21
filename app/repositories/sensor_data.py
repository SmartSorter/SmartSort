from sqlalchemy.orm import Session 
from app.models.sensor_data import SensorData 
from app.schemas.sensor_data import SensorDataCreate 

def get_sensor_data (db: Session, sensor_data_id: int):
    return db.query (SensorData).filter (SensorData.id==sensor_data_id).first ()

def get_all_sensor_data (db: Session, skip: int=0, limit: int=100):
    return db.query (SensorData).offset (skip).limit (limit).all ()

def create_sensor_data (db: Session, sensor_data: SensorDataCreate):
    db_sensor_data=SensorData (container_id=sensor_data.container_id, fill_level=sensor_data.fill_level)
    db.add (db_sensor_data)
    db.commit ()
    db.refresh (db_sensor_data)
    return db_sensor_data 

from sqlalchemy import Column, Integer, ForeignKey, DateTime 
from app.database import Base 
from datetime import datetime 

class SensorData (Base):
    __tablename__="sensor_data"

    id=Column (Integer, primary_key=True)
    container_id=Column (Integer, ForeignKey ("containers.id"), nullable=False)
    fill_level=Column (Integer, nullable=False)
    created_at=Column (DateTime, default=datetime.utcnow)

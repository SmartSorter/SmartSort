from sqlalchemy import Column, Integer, ForeignKey, String, DateTime 
from datetime import datetime 
from app.database import Base 

class Alert (Base):
    __tablename__="alerts"

    id=Column (Integer, primary_key=True)
    container_id=Column (Integer, ForeignKey ("containers.id"), nullable=False)
    message=Column (String (255), nullable=False)
    created_at=Column (DateTime, default=datetime.utcnow)

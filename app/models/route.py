from sqlalchemy import Column, Integer, String, DateTime 
from datetime import datetime 
from app.database import Base 

class Route (Base):
    __tablename__="routes"

    id=Column (Integer, primary_key=True)
    description=Column (String (255))
    created_at=Column (DateTime, default=datetime.utcnow)

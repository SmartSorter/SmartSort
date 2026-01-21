from sqlalchemy import Column, Integer, String, Boolean 
from app.database import Base 

class Device (Base):
    __tablename__="devices"

    id=Column (Integer, primary_key=True)
    serial_number=Column (String (100), unique=True, nullable=False)
    location=Column (String (255))
    is_active=Column (Boolean, default=True)

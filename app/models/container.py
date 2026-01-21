from sqlalchemy import Column, Integer, ForeignKey 
from app.database import Base 

class Container (Base):
    __tablename__="containers"

    id=Column (Integer, primary_key=True)
    device_id=Column (Integer, ForeignKey ("devices.id"), nullable=False)
    waste_type_id=Column (Integer, ForeignKey ("waste_types.id"), nullable=False)
    fill_level=Column (Integer, nullable=False)

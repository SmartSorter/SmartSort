from sqlalchemy import Column, Integer, String 
from app.database import Base 

class WasteType (Base):
    __tablename__="waste_types"

    id=Column (Integer, primary_key=True)
    name=Column (String (50), unique=True, nullable=False)

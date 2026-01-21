from pydantic import BaseModel 
from datetime import datetime 

class SensorDataBase (BaseModel):
    container_id: int 
    fill_level: int 

class SensorDataCreate (SensorDataBase):
    pass 

class SensorDataResponse (SensorDataBase):
    id: int 
    created_at: datetime 

    class Config:
        from_attributes=True 

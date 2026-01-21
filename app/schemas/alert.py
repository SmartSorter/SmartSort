from pydantic import BaseModel 
from datetime import datetime 
from typing import Optional 

class AlertBase (BaseModel):
    container_id: int 
    message: str 

class AlertCreate (AlertBase):
    pass 

class AlertResponse (AlertBase):
    id: int 
    created_at: datetime 

    class Config:
        from_attributes=True 

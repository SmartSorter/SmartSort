from pydantic import BaseModel 
from typing import Optional 

class DeviceBase (BaseModel):
    serial_number: str 
    location: Optional [str]=None 
    is_active: bool=True 

class DeviceCreate (DeviceBase):
    pass 

class DeviceUpdate (BaseModel):
    location: Optional [str]=None 
    is_active: Optional [bool]=None 

class DeviceResponse (DeviceBase):
    id: int 

    class Config:
        from_attributes=True 

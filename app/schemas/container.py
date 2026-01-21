from pydantic import BaseModel 
from typing import Optional 

class ContainerBase (BaseModel):
    fill_level: int=0 

class ContainerCreate (ContainerBase):
    device_id: int 
    waste_type_id: int 

class ContainerUpdate (BaseModel):
    fill_level: int 

class ContainerResponse (ContainerBase):
    id: int 
    device_id: int 
    waste_type_id: int 

    class Config:
        from_attributes=True 

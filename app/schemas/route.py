from pydantic import BaseModel 
from datetime import datetime 
from typing import Optional 

class RouteBase (BaseModel):
    description: Optional [str]=None 

class RouteCreate (RouteBase):
    pass 

class RouteResponse (RouteBase):
    id: int 
    created_at: datetime 

    class Config:
        from_attributes=True 

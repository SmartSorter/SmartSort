from pydantic import BaseModel 

class WasteTypeBase (BaseModel):
    name: str 

class WasteTypeCreate (WasteTypeBase):
    pass 

class WasteTypeResponse (WasteTypeBase):
    id: int 

    class Config:
        from_attributes=True 

from pydantic import BaseModel
from typing import Optional


class AnimalBase(BaseModel):
    name: str  
    description: str 
    picture: str
    enclos_id: int  
    admin_id: int  


class AnimalCreate(AnimalBase):
    pass

class AnimalUpdate(BaseModel):
    name: Optional[str] = None  
    description: Optional[str] = None  
    picture: Optional[str] = None  
    enclos_id: Optional[int] = None  
    admin_id: Optional[int] = None  

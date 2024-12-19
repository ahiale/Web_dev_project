from datetime import time
from pydantic import BaseModel
from typing import Optional


class EnclosBase(BaseModel):
    name: str  
    heuresD: time
    heuresF: time
    statut: bool
    admin_id: int  
    biome_id:int

class EnclosCreate(EnclosBase):
    pass


class EnclosUpdate(BaseModel):
    name: Optional[str] = None  
    heuresD: Optional[time]=None
    heuresF: Optional[time]=None
    statut: Optional[bool] = None  
   

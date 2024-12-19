from pydantic import BaseModel
from typing import Optional

class CompteBase(BaseModel):
    numero_compte: str  
    solde:float
   
    
class CompteCreate(CompteBase):
    pass


class CompteUpdate(BaseModel):
    solde: Optional[str] = None  
    numero_compte: Optional[str] = None  
     
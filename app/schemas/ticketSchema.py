from pydantic import BaseModel
from typing import Optional
from datetime import date

class TicketBase(BaseModel):
    qte: Optional[int] = None  
    user_id: int  
    compte_id:int
    dateticket:date

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    qte: Optional[int] = None
    dateticket: Optional[date] = None
    
    

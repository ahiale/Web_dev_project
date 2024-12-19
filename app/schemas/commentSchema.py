from pydantic import BaseModel
from typing import Optional

class CommentBase(BaseModel):
    content: str  
    user_id: int  
    enclos_id: int 


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: Optional[str] = None  
     
    

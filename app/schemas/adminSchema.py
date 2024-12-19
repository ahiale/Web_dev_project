from datetime import time
from pydantic import BaseModel
from typing import  Optional

class AdminBase(BaseModel):
    name: str  
    email: str  
    password: str  


class AdminCreate(AdminBase):
    pass


class AdminUpdate(BaseModel):
    name: Optional[str] = None  
    email: Optional[str] = None  
    password: Optional[str] = None  

class AdminToken(BaseModel):
    access_token: str
    token_type: str
    

class DataToken(BaseModel):
    id: Optional[str] = None
    

class AdminOutput(BaseModel):
    email: str
    id: str
    created_at: time
    
    class Config:
        orm_mode = True


class LoginSchema(BaseModel):
    email: str
    password: str


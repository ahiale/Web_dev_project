from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import time

class UserBase(BaseModel):
    name: str
    firstname:str
    email: EmailStr
    

class UserCreate(UserBase):
    password: str
    

class UserUpdate(BaseModel):
    name: Optional[str] = None
    firstname: Optional[int] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    

class UserToken(BaseModel):
    access_token: str
    token_type: str
    

class DataToken(BaseModel):
    id: Optional[str] = None
    

class UserOutput(BaseModel):
    email: str
    id: int
    created_at: time
    
    class Config:
        orm_mode = True


class LoginSchema(BaseModel):
    email: str
    password: str

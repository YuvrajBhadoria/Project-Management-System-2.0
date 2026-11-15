from pydantic import BaseModel,EmailStr
from uuid import UUID
from datetime import datetime

class Users(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    
class userResponse(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    
class CreateUser(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    password: str
    full_name: str
    is_active: bool
    created_at: datetime

class UserLogin(BaseModel):
    username: str
    password: str
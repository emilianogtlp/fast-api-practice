from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

# Class for the input of information

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #If the user does not provide a value, de default is True
    

class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    id: Optional[str] = None

# Class for the response (hides sensitive data, ej.passwords, dates, etc)

class ResponsePost(PostBase): #inherits from PostBase title, content and published
    idPost: int
    created_at: datetime
    idUser: int

    class Config: # Needed to be able to send something that is not a dict
        orm_mode = True

class ResponseUser(BaseModel):
    idUser: int
    email:EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
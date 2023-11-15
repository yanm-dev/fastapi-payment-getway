from typing import Optional, Union
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, validator
from models.user_model import UserModel


class UserAuth(BaseModel):
    pass

class RegisterSchema(BaseModel):
    first_name: str 
    last_name: str 
    email: EmailStr
    password: str 
    status_id: int
    created_by: int 


class UserOut(BaseModel):
    user_id: UUID
    first_name: str
    last_name: Optional[str]
    email: EmailStr
    password: Optional[str]
    status_id: int
    created_at: int


class LoginPost(BaseModel):
    username:str
    password:str


class GeneratePost(BaseModel):
    email:Union[str, None] = None
    phone:Union[str, None] = None
    password:Union[str, None] = None

class VerifyPost(BaseModel):
    otp_id:Union[str, None]=None
    code:Union[str, None]=None
    email:Union[str, None]=None
    phone_number:Union[str, None]=None

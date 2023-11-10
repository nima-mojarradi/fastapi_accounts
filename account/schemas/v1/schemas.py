from pydantic import BaseModel, EmailStr, constr
from fastapi.exceptions import HTTPException


class UserSignUp(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password1: str
    password2: str


class UserResponse(BaseModel):
    username: str


class UserLogin(BaseModel):
    username: str
    password: str


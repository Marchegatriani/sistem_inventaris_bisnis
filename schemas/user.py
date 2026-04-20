from pydantic import BaseModel
from typing import Optional
from models.user import UserRole

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.karyawan

class UserResponse(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    role: UserRole
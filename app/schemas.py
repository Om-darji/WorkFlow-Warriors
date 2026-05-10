from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

# --- Trip Schemas ---
class TripBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    total_budget: float = 0.0

class TripCreate(TripBase):
    pass

class TripResponse(TripBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True
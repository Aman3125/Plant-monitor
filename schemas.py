from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime

# Keep this list the same as the SENSORS dictionary in main.py
SensorName = Literal["temperature", "humidity", "light"]


class ReadingBase(BaseModel):
    sensor: SensorName
    content: float


class ReadingCreate(ReadingBase):
    user_id: int  # Temporary


class ReadingResponse(ReadingBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    date_timestamp: datetime
    author: UserResponse


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr = Field(max_length=320)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

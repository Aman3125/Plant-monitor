from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime

# Keep this list the same as the SENSORS dictionary in main.py
SensorName = Literal["temperature", "humidity", "light"]


# The data checks for requests and responses. FastAPI rejects anything that does not fit.

# Fields every reading has
class ReadingBase(BaseModel):
    sensor: SensorName
    content: float


# No user_id here: the reading is saved under the logged-in user
class ReadingCreate(ReadingBase):
    pass


# What the API sends back for a reading, including who sent it
class ReadingResponse(ReadingBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    date_timestamp: datetime
    author: UserResponse


# Fields every user has
class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr = Field(max_length=320)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)  # Password must be 8 to 128 characters


# What the API sends back for a user (never the password)
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# What the login endpoint sends back
class Token(BaseModel):
    access_token: str
    token_type: str

from pydantic import BaseModel
from typing import Optional
import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    phone: str
    name: Optional[str]
    password: Optional[str]

class UserOut(BaseModel):
    id: int
    phone: str
    name: Optional[str]
    is_driver: bool
    class Config:
        orm_mode = True

class RideCreate(BaseModel):
    pickup_lat: float
    pickup_lng: float
    dropoff_lat: float
    dropoff_lng: float

class RideOut(BaseModel):
    id: int
    rider_id: int
    driver_id: Optional[int]
    status: str
    fare: Optional[float]
    created_at: datetime.datetime
    class Config:
        orm_mode = True

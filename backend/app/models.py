from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)
    is_driver = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    driver = relationship("Driver", uselist=False, back_populates="user")

class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    license_no = Column(String, nullable=True)
    status = Column(String, default="pending")
    vehicle_plate = Column(String, nullable=True)
    user = relationship("User", back_populates="driver")

class Ride(Base):
    __tablename__ = "rides"
    id = Column(Integer, primary_key=True, index=True)
    rider_id = Column(Integer, ForeignKey("users.id"))
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    pickup_lat = Column(Float)
    pickup_lng = Column(Float)
    dropoff_lat = Column(Float)
    dropoff_lng = Column(Float)
    status = Column(String, default="requested")
    fare = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    ride_id = Column(Integer, ForeignKey("rides.id"))
    amount = Column(Float)
    method = Column(String)
    transaction_id = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

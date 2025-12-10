from sqlalchemy.orm import Session
from app import models, schemas
from app.core.security import get_password_hash

def create_user(db: Session, user_in: schemas.UserCreate):
    user = models.User(phone=user_in.phone, name=user_in.name)
    if user_in.password:
        user.hashed_password = get_password_hash(user_in.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone==phone).first()

def create_ride(db: Session, rider_id: int, ride_in: schemas.RideCreate):
    r = models.Ride(rider_id=rider_id, pickup_lat=ride_in.pickup_lat, pickup_lng=ride_in.pickup_lng, dropoff_lat=ride_in.dropoff_lat, dropoff_lng=ride_in.dropoff_lng)
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

def assign_driver(db: Session, ride_id: int, driver_id: int):
    r = db.query(models.Ride).get(ride_id)
    r.driver_id = driver_id
    r.status = "accepted"
    db.commit()
    db.refresh(r)
    return r

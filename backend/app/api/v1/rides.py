from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.deps import get_db
import json
import aioredis
from app.config import settings

router = APIRouter()

@router.post('/request', response_model=schemas.RideOut)
async def request_ride(ride_in: schemas.RideCreate, rider_id: int, db: Session = Depends(get_db)):
    ride = crud.create_ride(db, rider_id, ride_in)
    # publish to redis channel for matching worker
    redis = await aioredis.from_url(f"redis://{settings.REDIS_HOST}:6379", encoding="utf-8", decode_responses=True)
    await redis.publish("ride_requests", json.dumps({
        "ride_id": ride.id,
        "pickup_lat": ride.pickup_lat,
        "pickup_lng": ride.pickup_lng
    }))
    return ride

@router.post('/{ride_id}/assign')
def assign(ride_id: int, driver_id: int, db: Session = Depends(get_db)):
    ride = crud.assign_driver(db, ride_id, driver_id)
    return ride

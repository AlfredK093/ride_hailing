from fastapi import APIRouter, Request, Depends
from app.deps import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/webhook/airtel')
async def airtel_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    # Validate signature (aggregator) -> update Payment and Ride
    # TODO: implement verification logic
    return {'ok': True}

@router.post('/webhook/tnm')
async def tnm_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    # Validate and process
    return {'ok': True}

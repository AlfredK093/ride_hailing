from fastapi import APIRouter, Request, Depends, Header, HTTPException
from app.deps import get_db
from sqlalchemy.orm import Session
from app import models
import os
import hmac
import hashlib

router = APIRouter()


def verify_signature(secret: str, payload_bytes: bytes, signature_header: str) -> bool:
    if not secret or not signature_header:
        return False
    mac = hmac.new(secret.encode('utf-8'), payload_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, signature_header)


@router.post('/webhook/airtel')
async def airtel_webhook(request: Request, x_signature: str | None = Header(None), db: Session = Depends(get_db)):
    body = await request.body()
    try:
        # If a PAYMENT_SECRET is configured, verify signature header `X-Signature`
        secret = os.getenv('PAYMENT_SECRET')
        if secret:
            if not verify_signature(secret, body, x_signature or ''):
                raise HTTPException(status_code=400, detail='invalid signature')

        payload = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'invalid payload: {e}')

    # Basic processing: create/update Payment and mark Ride as paid when possible
    try:
        ride_id = payload.get('ride_id')
        amount = payload.get('amount')
        tx_id = payload.get('transaction_id') or payload.get('tx_id')
        method = 'airtel'

        if not ride_id:
            raise HTTPException(status_code=400, detail='missing ride_id')

        ride = db.query(models.Ride).get(ride_id)
        if not ride:
            raise HTTPException(status_code=404, detail='ride not found')

        payment = models.Payment(ride_id=ride_id, amount=amount or 0, method=method, transaction_id=tx_id, status='completed')
        db.add(payment)
        # update ride
        ride.status = 'paid'
        if amount:
            ride.fare = amount

        db.commit()
        return {'ok': True}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'processing error: {e}')


@router.post('/webhook/tnm')
async def tnm_webhook(request: Request, db: Session = Depends(get_db)):
    # For now handle similarly to airtel; aggregator-specific verification can be added
    body = await request.body()
    try:
        payload = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'invalid payload: {e}')

    try:
        ride_id = payload.get('ride_id')
        amount = payload.get('amount')
        tx_id = payload.get('transaction_id') or payload.get('tx_id')
        method = 'tnm'

        if not ride_id:
            raise HTTPException(status_code=400, detail='missing ride_id')

        ride = db.query(models.Ride).get(ride_id)
        if not ride:
            raise HTTPException(status_code=404, detail='ride not found')

        payment = models.Payment(ride_id=ride_id, amount=amount or 0, method=method, transaction_id=tx_id, status='completed')
        db.add(payment)
        ride.status = 'paid'
        if amount:
            ride.fare = amount

        db.commit()
        return {'ok': True}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'processing error: {e}')

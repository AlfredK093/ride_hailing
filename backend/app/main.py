from fastapi import FastAPI
from app.db import engine
from app import models
from app.api.v1 import auth, rides, payments
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Malawi Ride-Hailing API")

app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(rides.router, prefix="/api/v1/rides")
app.include_router(payments.router, prefix="/api/v1/payments")

@app.get("/")
def health():
    return {"status": "ok"}

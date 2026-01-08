import os
import json
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app import models
from app.db import Base
from app.deps import get_db


@pytest.fixture
def db_session():
    # use in-memory sqlite for tests
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_airtel_webhook_creates_payment_and_marks_ride_paid(db_session):
    # override the dependency
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    # create a ride to be paid
    ride = models.Ride(rider_id=1, pickup_lat=-1.0, pickup_lng=36.0, dropoff_lat=-1.1, dropoff_lng=36.1)
    db_session.add(ride)
    db_session.commit()
    db_session.refresh(ride)

    payload = {
        "ride_id": ride.id,
        "amount": 15.5,
        "transaction_id": "tx-12345"
    }

    resp = client.post("/api/v1/payments/webhook/airtel", json=payload)
    assert resp.status_code == 200
    assert resp.json().get('ok') is True

    # verify payment created and ride updated
    payments = db_session.query(models.Payment).filter(models.Payment.ride_id == ride.id).all()
    assert len(payments) == 1
    payment = payments[0]
    assert payment.amount == 15.5

    updated_ride = db_session.query(models.Ride).get(ride.id)
    assert updated_ride.status == 'paid'
    assert updated_ride.fare == 15.5

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.deps import get_db
from app.core.security import create_access_token, verify_password

router = APIRouter()

@router.post('/register', response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_phone(db, user_in.phone)
    if existing:
        raise HTTPException(400, "Phone already registered")
    user = crud.create_user(db, user_in)
    return user

@router.post('/login')
def login(phone: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_phone(db, phone)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    access = create_access_token({"sub": str(user.id)})
    return {"access_token": access, "token_type": "bearer"}

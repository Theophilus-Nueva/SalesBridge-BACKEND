from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from security import create_access_token
from schemas import Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    booking_id = form_data.username  
    
    access_token = create_access_token(data={"sub": booking_id})
    return {"access_token": access_token, "token_type": "bearer"}
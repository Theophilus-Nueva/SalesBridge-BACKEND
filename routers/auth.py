from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from security import create_access_token
from models import Customer, Booking

router = APIRouter(prefix="/auth", tags=["auth"])

MAX_ATTEMPTS = 3 

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.email == form_data.username).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
        
    if customer.failed_attempts >= MAX_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Account temporarily locked due to too many failed attempts."
        )
    
    if customer.password != form_data.password:
        
        customer.failed_attempts += 1
        db.commit()
        
        attempts_left = MAX_ATTEMPTS - customer.failed_attempts
        
        if attempts_left <= 0:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Account locked out. Please try again later."
            )
            
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Incorrect password. You have {attempts_left} attempts left."
        )
        
    customer.failed_attempts = 0
    db.commit()
        
    booking = db.query(Booking).filter(
        Booking.customer_id == customer.customer_id
    ).order_by(Booking.booking_date.desc()).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No active bookings found."
        )

    access_token = create_access_token(data={"sub": f"{booking.booking_id}"})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "name": customer.customer_name,
        "booking_id": booking.booking_id
    }
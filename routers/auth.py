from fastapi import APIRouter, Depends, HTTPException, status, Request 
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from security import create_access_token, limiter 
from models import Customer, Booking

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
@limiter.limit("3/minute") 
def login(
    request: Request, 
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(Customer.email == form_data.username).first()
    
    if not customer or customer.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
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
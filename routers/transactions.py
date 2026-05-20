from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from models import TransactionHeader, TransactionDetails, Product
from schemas import TransactionResponse
from security import get_current_user, limiter
from typing import List

router = APIRouter(prefix="/api/transactions", tags=["transactions"])

@router.get("/", response_model=List[TransactionResponse])
@limiter.limit("60/minute")
def get_transactions(
    request: Request, 
    booking_id: int = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            TransactionDetails.detail_id, 
            TransactionHeader.transaction_date, 
            Product.product_name, 
            TransactionDetails.amount
        )
        .join(TransactionHeader, TransactionDetails.transaction_id == TransactionHeader.transaction_id)
        .join(Product, TransactionDetails.product_id == Product.product_id)
        .filter(TransactionHeader.booking_id == booking_id)
        .all()
    )
    
    return [
        {
            "id": row.detail_id,
            "date": row.transaction_date.strftime("%Y-%m-%d"),
            "item": row.product_name,
            "amount": float(row.amount)
        }
        for row in results
    ]
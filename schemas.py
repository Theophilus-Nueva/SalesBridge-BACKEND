from pydantic import BaseModel
from typing import List

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    booking_id: int | None = None

class TransactionResponse(BaseModel):
    id: int
    date: str
    item: str
    amount: float

    class Config:
        orm_mode = True
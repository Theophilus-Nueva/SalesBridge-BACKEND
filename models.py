from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date, Text
from database import Base
from datetime import datetime

class Customer(Base):
    __tablename__ = "customer"
    customer_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    password = Column(String(100))

class Room(Base):
    __tablename__ = "room"
    room_id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(10))
    room_type = Column(String(50))
    bed_type = Column(String(50))
    no_of_beds = Column(Integer)
    guests = Column(Integer)

class Schedule(Base):
    __tablename__ = "schedule"
    schedule_id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("room.room_id"))
    check_in = Column(Date)
    check_out = Column(Date)

class Booking(Base):
    __tablename__ = "booking"
    booking_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))
    schedule_id = Column(Integer, ForeignKey("schedule.schedule_id"))
    booking_date = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100))
    stock = Column(Integer)
    price = Column(Float)
    description = Column(Text)
    product_image = Column(String(255))

class TransactionHeader(Base):
    __tablename__ = "transactionheader"
    transaction_id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("booking.booking_id"))
    subtotal = Column(Float)
    vat = Column(Float)
    total = Column(Float)
    transaction_date = Column(DateTime, default=datetime.utcnow)

class TransactionDetails(Base):
    __tablename__ = "transactiondetails"
    detail_id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactionheader.transaction_id"))
    product_id = Column(Integer, ForeignKey("product.product_id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    amount = Column(Float)
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Customer(Base):
    __tablename__ = "Customer"
    customer_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))

class Room(Base):
    __tablename__ = "Room"
    room_id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(10))
    room_type = Column(String(50))
    bed_type = Column(String(50))
    no_of_beds = Column(Integer)
    guests = Column(Integer)

class Schedule(Base):
    __tablename__ = "Schedule"
    schedule_id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("Room.room_id"))
    check_in = Column(Date)
    check_out = Column(Date)

class Booking(Base):
    __tablename__ = "Booking"
    booking_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("Customer.customer_id"))
    schedule_id = Column(Integer, ForeignKey("Schedule.schedule_id"))
    booking_date = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = "Product"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100))
    stock = Column(Integer)
    price = Column(Float)
    description = Column(Text)
    product_image = Column(String(255))

class TransactionHeader(Base):
    __tablename__ = "TransactionHeader"
    transaction_id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("Booking.booking_id"))
    subtotal = Column(Float)
    vat = Column(Float)
    total = Column(Float)
    transaction_date = Column(DateTime, default=datetime.utcnow)

class TransactionDetails(Base):
    __tablename__ = "TransactionDetails"
    detail_id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("TransactionHeader.transaction_id"))
    product_id = Column(Integer, ForeignKey("Product.product_id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    amount = Column(Float)
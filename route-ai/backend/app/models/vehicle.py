from sqlalchemy import Column, String, Float
from app.database.base import Base

class Vehicle(Base):
    __tablename__ = 'vehicles'
    id = Column(String, primary_key=True)
    license_plate = Column(String, unique=True)
    capacity_kg = Column(Float)

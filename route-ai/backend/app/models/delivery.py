from sqlalchemy import Column, String, Float
from app.database.base import Base

class Delivery(Base):
    __tablename__ = 'deliveries'
    id = Column(String, primary_key=True)
    destination = Column(String)
    status = Column(String, default='pending')

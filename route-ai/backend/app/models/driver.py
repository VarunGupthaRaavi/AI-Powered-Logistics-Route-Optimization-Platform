from sqlalchemy import Column, String, Boolean
from app.database.base import Base

class Driver(Base):
    __tablename__ = 'drivers'
    id = Column(String, primary_key=True)
    name = Column(String)
    status = Column(String, default='available')

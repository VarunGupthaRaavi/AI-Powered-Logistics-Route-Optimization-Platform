from sqlalchemy import Column, String, Float
from app.database.base import Base

class Route(Base):
    __tablename__ = 'routes'
    id = Column(String, primary_key=True)
    status = Column(String, default='planned')

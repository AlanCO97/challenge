from sqlalchemy import Column, Integer, String
from db import Base

# Modelo pasajero
class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40), nullable=False)
    email = Column(String(40), nullable=False, unique=True)
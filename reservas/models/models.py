from sqlalchemy import Column, ForeignKey, Integer, String, func, DateTime
from sqlalchemy.orm import relationship
from db import Base

class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40), nullable=False)
    email = Column(String(40), nullable=False, unique=True)

    reservations = relationship("Reservation", back_populates="passenger")

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    passenger_id = Column(Integer, ForeignKey("passengers.id"))
    name = Column(String(40), nullable=False)
    created_at = Column(DateTime, default=func.now())


    # When we acces to the passenger attribute on Reservation it will fetch the passenger.
    passenger = relationship("Passenger", back_populates="reservations")
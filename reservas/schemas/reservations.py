from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from schemas.passengers import Passenger, PassengerCreate, PassengerUpdate

class ReservationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    created_at: Optional[datetime] = None

class ReservationCreate(ReservationBase):
    passenger: PassengerCreate

class ReservationUpdate(ReservationBase):
    id: int
    passenger: PassengerUpdate

class Reservation(ReservationBase):
    id: int
    passenger: Passenger
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

class PassengerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    email: EmailStr

class PassengerCreate(PassengerBase):
    pass

class PassengerUpdate(PassengerBase):
    id: Optional[int] = None

class Passenger(PassengerBase):
    id: int
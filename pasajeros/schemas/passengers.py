from pydantic import BaseModel, ConfigDict, EmailStr

# Schemas para validacion de datos y request body
class PassengerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    email: EmailStr

class PassengerSchema(PassengerBase):
    id: int
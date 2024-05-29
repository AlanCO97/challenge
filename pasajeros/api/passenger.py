from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.passengers import PassengerSchema
from services.passenger import PassengerService
from repositories.passenger import PassengerRepository
from db import get_db

router = APIRouter()

passenger_repository = PassengerRepository()
passenger_service = PassengerService(passenger_repository)

# Route para optener todos los pasajeros
@router.get("/passengers", response_model=List[PassengerSchema])
def get_all(db: Session = Depends(get_db)):
    passengers = passenger_service.get_all(db)
    return passengers
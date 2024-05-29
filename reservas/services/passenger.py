from typing import List
from sqlalchemy.orm import Session

from repositories.passenger import PassengerRepository
from schemas.passengers import PassengerCreate

class PassengerService:
    def __init__(self, passenger_repository: PassengerRepository) -> None:
        self.passenger_repository = passenger_repository
    
    def bulk_create(self, db: Session, passengers: List[PassengerCreate]):
        return self.passenger_repository.bulk_create(db, passengers)
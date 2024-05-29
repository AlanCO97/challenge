from typing import List
from schemas.reservations import ReservationCreate, ReservationUpdate
from repositories.reservation import ReservationRepository
from sqlalchemy.orm import Session

class ReservationService:
    def __init__(self, reservation_repository: ReservationRepository) -> None:
        self.reservation_repository = reservation_repository
    
    def create(self, db: Session, reservation: ReservationCreate):
        return self.reservation_repository.create(db, reservation)
    
    def get_all(self, db: Session):
        return self.reservation_repository.get_all(db)
    
    def get_by_id(self, db: Session, reservation_id: int):
        return self.reservation_repository.get_by_id(db, reservation_id)
    
    def update(self, db: Session, reservation_id: int, reservation: ReservationUpdate):
        return self.reservation_repository.update(db, reservation_id, reservation)
    
    def delete(self, db: Session, reservation_id: int):
        return self.reservation_repository.delete(db, reservation_id)

    def bulk_create(self, db: Session, reservations: List[ReservationCreate]):
        return self.reservation_repository.bulk_create(db, reservations)
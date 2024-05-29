from typing import List
from schemas.passengers import PassengerSchema
from repositories.passenger import PassengerRepository
from sqlalchemy.orm import Session

# Servicio para mandar a llamar el repositorio de pasajeros
class PassengerService:
    def __init__(self, passenger_repository: PassengerRepository) -> None:
        self.passenger_repository = passenger_repository
    # Manda a llamar la creacion de un pasajero en la base de datos
    def create(self, db: Session, passenger: PassengerSchema):
        return self.passenger_repository.create(db, passenger)
    # Manda a llamar a todos los pasajeros de la base de datos
    def get_all(self, db: Session) -> List[PassengerSchema]:
        return self.passenger_repository.get_all(db)
    # Manda a llamar el update de un pasajero en la base de datos
    def update(self, db: Session, passenger: PassengerSchema):
        return self.passenger_repository.update(db, passenger)
    # Manda a llamar el delete de un pasajero a la base de datos
    def delete(self, db: Session, passenger_id: int):
        return self.passenger_repository.delete(db, passenger_id)
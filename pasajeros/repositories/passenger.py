from typing import List
from sqlalchemy.orm import Session
from models.passenger import Passenger
from schemas.passengers import PassengerSchema

class PassengerRepository:
    # funcion que crea un pasajero en la db
    def create(self, db: Session, passenger: PassengerSchema):
        try:
            with db.begin():
                # Verificar si el pasajero existe
                db_passenger = db.query(Passenger).filter(Passenger.email == passenger.email).first()
                
                if not db_passenger:
                    db_passenger = Passenger(
                        id=passenger.id,
                        name=passenger.name,
                        email=passenger.email
                    )
                    db.add(db_passenger)
                    db.flush()
                    db.refresh(db_passenger)
                
                return db_passenger
        except Exception as e:
            raise e
    # funcion que crea obtiene todos los pasajeros
    def get_all(self, db: Session) -> List[PassengerSchema]:
        try:
            # Realizar la consulta para obtener todos los pasajeros
            reservations = db.query(Passenger).all()
            return reservations
        except Exception as e:
            raise e
    # funcion que actualiza un pasajero
    def update(self, db: Session, passenger: PassengerSchema):
        try:
            with db.begin():

                # Verificar si el pasajero ya existe por correo electrónico
                db_passenger = db.query(Passenger).filter(Passenger.email == passenger.email).first()

                if not db_passenger:
                    raise ValueError(f"No passenger was found")

                # Actualizar los datos
                db_passenger.name = passenger.name

                db.commit()
                return db_passenger
        except Exception as e:
            raise e
    # funcion que elimina un pasajero
    def delete(self, db: Session, passenger_id: int) -> None:
        try:
            with db.begin():
                # Verificar si existe una reservacion
                existing_passenger = db.query(Passenger).filter(Passenger.id == passenger_id).first()
                if not existing_passenger:
                    raise ValueError(f"Passenger not found")

                # Eliminar el pasajero
                db.query(Passenger).filter(Passenger.id == passenger_id).delete()

                db.commit()
        except Exception as e:
            raise e
        
    
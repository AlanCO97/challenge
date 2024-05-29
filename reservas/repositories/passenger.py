from typing import List
from sqlalchemy.orm import Session

from models.models import Passenger
from schemas.passengers import PassengerCreate

class PassengerRepository:
    def bulk_create(self, db: Session, passengers: List[PassengerCreate]):
        try:
            with db.begin():
                created_passengers = []
                # Se remueven los pasajeros con email duplicado duplicados
                passenger_emails = set([passenger.email for passenger in passengers])

                # Obtenemos los pasajeros que ya existen con base en passenger_emails
                existing_passengers = db.query(Passenger).filter(Passenger.email.in_(passenger_emails)).all()
                # Hacemos una list con los correos de los pasajeros que ya existen
                existing_emails = set([passenger.email for passenger in existing_passengers])
                
                # Los que ya existen se agregan directamente al arreglo de created_passengers porque no se volveran a crear
                created_passengers.extend(existing_passengers)

                # Se crea una lista con los nuevos pasajeros
                new_passengers = [
                    Passenger(name=passenger.name, email=passenger.email)
                    for passenger in passengers if passenger.email not in existing_emails
                ]

                # Verificamos si hay nuevos pasajeros y si lo hay los creamos
                if new_passengers:
                    for passenger in new_passengers:
                        db.add(passenger)
                    
                    db.flush()
                    created_passengers.extend(new_passengers)

                return created_passengers
        except Exception as e:
            raise e
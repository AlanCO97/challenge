from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from models.models import Passenger, Reservation
from schemas.reservations import ReservationCreate, ReservationUpdate

class ReservationRepository:
    def create(self, db: Session, reservation: ReservationCreate):
        try:
            with db.begin():
                # Verificar si el pasajero existe
                db_passenger = db.query(Passenger).filter(Passenger.email == reservation.passenger.email).first()
                
                if not db_passenger:
                    db_passenger = Passenger(
                        name=reservation.passenger.name,
                        email=reservation.passenger.email
                    )
                    db.add(db_passenger)
                    db.flush()
                    db.refresh(db_passenger)
                
                # Crear la reserva asociada al pasajero
                db_reservation = Reservation(
                    name=reservation.name,
                    passenger_id=db_passenger.id
                )
                db.add(db_reservation)
                db.flush()
                db.refresh(db_reservation)
                return db_reservation
        except Exception as e:
            raise e
    
    def get_all(self, db: Session) -> List[Reservation]:
        try:
            # Realizar la consulta para obtener todas las reservaciones con sus pasajeros asociados
            reservations = db.query(Reservation).options(joinedload(Reservation.passenger)).all()
            return reservations
        except Exception as e:
            raise e
    
    def get_by_id(self, db: Session, reservation_id: int) -> Optional[Reservation]:
        try:
            # Realizar la consulta para obtener la reserva por su ID
            reservation = db.query(Reservation).filter(Reservation.id == reservation_id).options(joinedload(Reservation.passenger)).first()
            return reservation
        except Exception as e:
            raise e
    
    def update(self, db: Session, reservation_id: int, reservation: ReservationUpdate) -> Reservation:
        try:
            with db.begin():
                # Obtener la reserva existente por su ID
                db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
                if not db_reservation:
                    raise ValueError("Reservation not found")
                
                # Verificar si el pasajero ya existe por correo electrónico
                db_passenger = db.query(Passenger).filter(Passenger.email == reservation.passenger.email).first()

                if not db_passenger:
                    raise ValueError(f"Reservation {db_reservation.name} does not have passenger {reservation.passenger.name}")

                # Actualizar los datos
                db_passenger.name = reservation.passenger.name
                db_reservation.name = reservation.name
                db_reservation.passenger_id = db_passenger.id

                db.commit()
                return db_reservation
        except Exception as e:
            raise e
        
    def delete(self, db: Session, reservation_id: int) -> tuple[int, bool]:
        try:
            with db.begin():
                # Flag para ver si se elimino el pasajero
                passenger_delete: bool = False
                # Verificar si existe una reservación
                existing_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
                if not existing_reservation:
                    raise ValueError(f"Reservation with ID {reservation_id} not found")

                # Obtener el pasajero
                passenger_id = existing_reservation.passenger_id
                existing_passenger = db.query(Passenger).filter(Passenger.id == passenger_id).first()

                # Eliminar la reservación
                db.query(Reservation).filter(Reservation.id == reservation_id).delete()

                # Verificar cuántas reservaciones tiene el pasajero
                reservation_count = db.query(Reservation).filter(Reservation.passenger_id == passenger_id).count()

                # Eliminar al pasajero solo si no tiene otras reservaciones
                if existing_passenger and reservation_count == 0:
                    passenger_delete = True
                    db.delete(existing_passenger)

                db.commit()
                return passenger_id, passenger_delete
        except Exception as e:
            raise e
    
    def bulk_create(self, db: Session, reservations: List[ReservationCreate]):
        try:
            with db.begin():
                created_reservations = []
                passenger_cache = {}

                for reservation in reservations:
                    # Verificar si el pasajero existe en el cache
                    if reservation.passenger.email in passenger_cache:
                        db_passenger = passenger_cache[reservation.passenger.email]
                    else:
                        db_passenger = db.query(Passenger).filter(Passenger.email == reservation.passenger.email).first()
                        if not db_passenger:
                            db_passenger = Passenger(
                                name=reservation.passenger.name,
                                email=reservation.passenger.email
                            )
                            db.add(db_passenger)
                            db.flush()
                            db.refresh(db_passenger)
                        passenger_cache[reservation.passenger.email] = db_passenger

                    # Crear la reserva asociada al pasajero
                    db_reservation = Reservation(
                        name=reservation.name,
                        passenger_id=db_passenger.id
                    )
                    db.add(db_reservation)
                    db.flush()
                    db.refresh(db_reservation)
                    created_reservations.append(db_reservation)

                return created_reservations
        except Exception as e:
            raise e
        
    
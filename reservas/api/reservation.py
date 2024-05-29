from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.messaging import publish_message
from schemas.reservations import ReservationCreate, Reservation, ReservationUpdate
from services.reservation import ReservationService
from repositories.reservation import ReservationRepository
from db import get_db
import logging
import sys

router = APIRouter()

# Se crea un logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

# Se crea una instancia de nuestro repositorio que es el quue se encarga de hacer las consultas
reservation_repository = ReservationRepository()
# Se crea una instancia de nuetro servicio y le le pasa la instancia del repositorio
reservation_service = ReservationService(reservation_repository)

# Se restablece la ruta y como va a ser la response
@router.post("/reservations", response_model=Reservation)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    # Se manda a llamar el servicio de crear que a su ves recibe una instancia de una sesion de la base de datos y el objeto a crear
    db_reservation = reservation_service.create(db, reservation)
    if db_reservation is None:
        raise HTTPException(status_code=400, detail="not saved")

    # Creamos nuestro pasajero que es el que vamos a enviar a la queue
    passenger = {
        "id": db_reservation.passenger.id,
        "name": db_reservation.passenger.name,
        "email": db_reservation.passenger.email,
    }
    logger.info(f"Passenger {passenger} on create sent")
    # Establecemos el router_key y el mesaje para la queue
    publish_message("passenger_created", passenger)
    return db_reservation

@router.post("/reservations/bulk", response_model=List[Reservation])
def bulk_create(reservations: List[ReservationCreate], db: Session = Depends(get_db)):
    # Se manda a llamar el servicio de bulk_create que a su ves recibe una instancia de una sesion de la base de datos y el objeto a crear
    db_reservations = reservation_service.bulk_create(db, reservations)
    if db_reservations is None:
        raise HTTPException(status_code=400, detail="not saved")
    for reservation in db_reservations:
        # Creamos nuestro pasajero que es el que vamos a enviar a la queue
        passenger = {
            "id": reservation.passenger.id,
            "name": reservation.passenger.name,
            "email": reservation.passenger.email,
        }
        logger.info(f"Passenger {passenger} on create sent")
        # Establecemos el router_key y el mesaje para la queue
        publish_message("passenger_created", passenger)
    return db_reservations

@router.get("/reservations", response_model=List[Reservation])
def get_reservation(db: Session = Depends(get_db)):
    # Se manda a llamar el servicio de get_all que a su ves recibe una instancia de una sesion de la base de datos y este devuelve todas las reservaciones
    db_reservation = reservation_service.get_all(db)
    return db_reservation

@router.get("/reservations/{reservation_id}", response_model=Reservation)
def get_reservation_by_id(reservation_id: int, db: Session = Depends(get_db)):
    # Se manda a llamar el servicio de get_by_id que a su ves recibe una instancia de una sesion de la base de datos y el id de una reservacion para retornarla
    db_reservation = reservation_service.get_by_id(db, reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="not found")
    return db_reservation

@router.put("/reservations/{reservation_id}", response_model=Reservation)
def update_reservation(
    reservation_id: int,
    reservation_update: ReservationUpdate,
    db: Session = Depends(get_db)
):
    try:
        # Se manda a llamar el servicio de update que a su ves recibe una instancia de una sesion de la base de datos, el id de una reservacion y la nueva reservacion
        updated_reservation = reservation_service.update(db, reservation_id, reservation_update)
        passenger = {
            "id": updated_reservation.passenger.id,
            "name": updated_reservation.passenger.name,
            "email": updated_reservation.passenger.email,
        }
        logger.info(f"Passenger {passenger} updated sent")
        # Se envia el pasajero a la queue
        publish_message("passenger_updated", passenger)
        return updated_reservation
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    try:
        # Se manda a llamar el servicio de delete que a su ves recibe una instancia de una sesion de la base de datos, el id de una reservacion para eliminarla
        passenger_id, passenger_delete = reservation_service.delete(db, reservation_id)
        logger.info(f"Reservation {reservation_id} deleted")
        logger.info(f"Passenger id {passenger_id}")
        if passenger_delete:
            # Se manda el id para eliminarlo de la base de dartos del otro servicio
            publish_message("passenger_deleted", {"id": passenger_id})
        return {"message": "Reservation deleted successfully"}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
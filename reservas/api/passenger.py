from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.messaging import publish_message
from schemas.passengers import PassengerCreate, Passenger
from services.passenger import PassengerService
from repositories.passenger import PassengerRepository
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
passenger_repository = PassengerRepository()
# Se crea una instancia de nuetro servicio y le le pasa la instancia del repositorio
passenger_service = PassengerService(passenger_repository)

@router.post("/passengers/bulk", response_model=List[Passenger])
def bulk_create_passenger(passengers: List[PassengerCreate], db: Session = Depends(get_db)):
    # Se manda a llamar el servicio de bulk_create que a su ves recibe una instancia de una sesion de la base de datos y el objeto a crear
    db_passengers = passenger_service.bulk_create(db, passengers)
    if db_passengers is None:
        raise HTTPException(status_code=400, detail="not saved")
    for passenger in db_passengers:
        # Creamos nuestro pasajero que es el que vamos a enviar a la queue
        newPassenger = {
            "id": passenger.id,
            "name": passenger.name,
            "email": passenger.email,
        }
        logger.info(f"Passenger {newPassenger} on create sent")
        # Establecemos el router_key y el mesaje para la queue
        publish_message("passenger_created", newPassenger)
    return db_passengers
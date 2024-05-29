from fastapi import FastAPI
from api import reservation, passenger
from db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(reservation.router, prefix="/api")
app.include_router(passenger.router, prefix="/api")
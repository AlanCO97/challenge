from fastapi import FastAPI
from api import reservation
from db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(reservation.router, prefix="/api")
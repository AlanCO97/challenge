from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from api import passenger
from db import Base, engine
from core.messaging import connect_to_rabbitmq, close_rabbitmq


Base.metadata.create_all(bind=engine)

# Se crea un lifespan asincrono para que no bloquee el server
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cuando se inicia el server se hace la conexion a rabbitmq
    await connect_to_rabbitmq(app)
    yield
    # Cuando se pare de ejecutar el server se para el proceso de la conexion a rabbitmq
    await close_rabbitmq(app)

app = FastAPI(lifespan=lifespan)

# Se registran las rutas
app.include_router(passenger.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True, lifespan="on")
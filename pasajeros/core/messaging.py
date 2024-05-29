import asyncio
from functools import partial
import aio_pika
from fastapi import FastAPI
from db import get_db
from core.config import settings
import json

from schemas.passengers import PassengerSchema
from repositories.passenger import PassengerRepository
from services.passenger import PassengerService

# url de rabbitmq
RABBIT_MQ_URL = settings.RABBITMQ_URL

passenger_repository = PassengerRepository()
passenger_service = PassengerService(passenger_repository)

# Funcion que procesa los mensajes
async def process_message(db, message: aio_pika.IncomingMessage):
    async with message.process(ignore_processed=True):
        try:
            # procesa la creacion de pasajeros
            if message.routing_key == "passenger_created":
                json_body = json.loads(message.body)
                instance = PassengerSchema(id=json_body['id'],
                                   email=json_body['email'],
                                   name=json_body['name'])
                passenger_service.create(db, instance)
            # procesa la actualizacion
            if message.routing_key == "passenger_updated":
                json_body = json.loads(message.body)
                instance = PassengerSchema(id=json_body['id'],
                                   email=json_body['email'],
                                   name=json_body['name'])
                passenger_service.update(db, instance)
            # procesa la eliminacion de pasajeros
            if message.routing_key == "passenger_deleted":
                json_body = json.loads(message.body)
                passenger_service.delete(db, json_body['id'])
            # Se reconoce el mensaje
            await message.ack()
        except Exception as e:
            print(f"Error processing message: {e}")
            # Si hay un error se devuelve el mensaje a la cola
            await message.nack(requeue=True)

async def listener(loop, db):
    # Se crea la conexion
    connection = await aio_pika.connect_robust(
        RABBIT_MQ_URL, loop=loop
    )

    # se crea el canal
    channel = await connection.channel()

    # No aceptará más de 1 mensajes por adelantado.
    await channel.set_qos(prefetch_count=1)

    # itero por las queue
    for event in ['passenger_created', 'passenger_updated', 'passenger_deleted']:
        # se declara la queue
        queue = await channel.declare_queue(event, durable=True)
        # se usa parcial para crear una nueva con los argumentos proporcionados
        process_message_partial = partial(process_message, db)
        # se empieza a consumir la queue y por cada mensaje se ejecuta process_message
        await queue.consume(process_message_partial)

    return connection

async def connect_to_rabbitmq(app: FastAPI):
    # se obtiene el event loop
    loop = asyncio.get_event_loop()
    # se obtiene la bd
    db = next(get_db())
    # el listener se almacena en app.state.rabbitmq, esto se hace para que se comparta el estado
    # por toda la aplicacion y cuando querramos cerrarla solo hagamos app.state.rabbitmq.close()
    app.state.rabbitmq = await listener(loop, db)

# funcion que cierra la conexion
async def close_rabbitmq(app: FastAPI):
    await app.state.rabbitmq.close()

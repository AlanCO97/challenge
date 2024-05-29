import pika
import json

from core.config import settings

def get_connection():
    return pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))

# Se hace la publicacion del mensaje de acuerdo al nombre del evento
def publish_message(event: str, message: dict):
    connection = get_connection()
    channel = connection.channel()

    # Declarar la cola como duradera
    channel.queue_declare(queue=event, durable=True)

    # Publicar el mensaje como persistente
    channel.basic_publish(
        exchange='',
        routing_key=event,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,  # Hace el mensaje persistente
        )
    )

    connection.close()
from unittest import mock
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, call
from core.messaging import listener

@pytest.mark.asyncio
async def test_listener():
    loop = asyncio.get_event_loop()
    db = AsyncMock()

    mock_connection = AsyncMock()
    mock_channel = AsyncMock()
    mock_queue = AsyncMock()
    RABBIT_MQ_URL="amqp://root:123@localhost/"

    events = ['passenger_created', 'passenger_updated', 'passenger_deleted']

    with patch("aio_pika.connect_robust", return_value=mock_connection) as mock_connect:
        mock_connection.channel.return_value = mock_channel
        mock_channel.declare_queue.return_value = mock_queue

        await listener(loop, db)

        # Verificar que se haya hecho la conexion
        mock_connect.assert_called_once_with(RABBIT_MQ_URL, loop=loop)
        
        # Verificar que se haya hecho el canal
        mock_connection.channel.assert_awaited_once()
        
        # Verificar que se estableció el QoS
        mock_channel.set_qos.assert_awaited_once_with(prefetch_count=1)
        
        # Verificar que se crearon todas las colas
        declare_calls = [call(event, durable=True) for event in events]
        mock_channel.declare_queue.assert_has_awaits(declare_calls, any_order=True)

        # Verificar que se hizo la llada del consume
        consume_calls = [call(mock.ANY) for _ in events]
        mock_queue.consume.assert_has_awaits(consume_calls, any_order=True)
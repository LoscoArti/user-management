import json

import aio_pika
import aio_pika.abc

from src.config import settings

rabbitmq_uri = settings.RABBITMQ_URI
routing_key = settings.rabbitmq_routing_key


async def message_sender(body: dict):
    body_json = json.dumps(body)
    connection = await aio_pika.connect_robust(rabbitmq_uri)

    channel: aio_pika.abc.AbstractChannel = await connection.channel()

    await channel.default_exchange.publish(
        aio_pika.Message(body=body_json.encode()),
        routing_key=routing_key,
    )

    await connection.close()

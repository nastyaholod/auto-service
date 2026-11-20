import aio_pika
import json
from app.infrastructure.database.config import RabbitMQConfig

class RabbitMQPublisher:
    def __init__(self):
        self._config = RabbitMQConfig()
        self._connection = None
        self._channel = None

    async def connect(self):
        self._connection = await aio_pika.connect_robust(self._config.dsn)
        self._channel = await self._connection.channel()
        await self._channel.declare_queue("work_order_events", durable=True)
        print("[RabbitMQ] Connected and queue declared")

    async def publish_work_order_created(self, event_data: dict):
        if not self._channel:
            await self.connect()
        
        message = aio_pika.Message(
            body=json.dumps(event_data).encode(),
            content_type="application/json"
        )
        await self._channel.default_exchange.publish(
            message,
            routing_key="work_order_events"
        )
        print(f"[RabbitMQ] Published event: {event_data['work_order_id']}")

    async def close(self):
        if self._connection:
            await self._connection.close()
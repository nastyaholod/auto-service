import asyncio
import json
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import aio_pika

from app.infrastructure.database.config import DatabaseConfig, RabbitMQConfig
from app.infrastructure.database.models import Base, InvoiceModel, InvoiceStatusEnum

async def process_message(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        body = json.loads(message.body.decode())
        print(f"[Billing Consumer] Получено событие: {body}")
        
        db_config = DatabaseConfig()
        engine = create_async_engine(db_config.dsn)
        session_factory = async_sessionmaker(engine)
        
        async with session_factory() as session:
            # Создаем счет на основе данных из события
            new_invoice = InvoiceModel(
                id=uuid.uuid4(),
                work_order_id=uuid.UUID(body["work_order_id"]),
                amount=body["total_amount"],
                status=InvoiceStatusEnum.PENDING,
                created_at=datetime.fromisoformat(body["created_at"])
            )
            session.add(new_invoice)
            await session.commit()
            print(f"[Billing Consumer] ✅ Счет создан для заказ-наряда {body['work_order_id']}")

async def main():
    rmq_config = RabbitMQConfig()
    db_config = DatabaseConfig()
    
    # Создаем таблицы при старте
    engine = create_async_engine(db_config.dsn)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("[Billing Consumer] Подключение к RabbitMQ...")
    connection = await aio_pika.connect_robust(rmq_config.dsn)
    channel = await connection.channel()
    
    # Объявляем ту же очередь, в которую пишет outbox-publisher
    queue = await channel.declare_queue("work_order_events", durable=True)
    
    print("[Billing Consumer] ✅ Слушаю очередь 'work_order_events'...")
    await queue.consume(process_message)
    
    # Держим скрипт запущенным
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
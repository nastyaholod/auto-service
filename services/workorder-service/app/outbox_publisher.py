import asyncio
import json
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.infrastructure.database.config import DatabaseConfig
from app.infrastructure.database.models import Base, OutboxEventModel
from app.infrastructure.rmq.publisher import RabbitMQPublisher
from sqlalchemy import select

async def publish_unpublished_events():
    db_config = DatabaseConfig()
    engine = create_async_engine(db_config.dsn)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    
    # Создаем таблицы при запуске
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    publisher = RabbitMQPublisher()
    await publisher.connect()
    
    print("[Outbox Publisher] Started polling for unpublished events...")
    
    while True:
        try:
            async with session_factory() as session:
                result = await session.execute(
                    select(OutboxEventModel).where(OutboxEventModel.published == False).limit(10)
                )
                events = result.scalars().all()
                
                if not events:
                    await asyncio.sleep(5)
                    continue
                
                for event in events:
                    try:
                        payload = json.loads(event.payload)
                        await publisher.publish_work_order_created(payload)
                        
                        # Помечаем как опубликованное
                        event.published = True
                        await session.commit()
                        print(f"[Outbox Publisher] ✅ Published event {event.id}")
                        
                    except Exception as e:
                        print(f"[Outbox Publisher] Error publishing event {event.id}: {e}")
                        await session.rollback()
        
        except Exception as e:
            print(f"[Outbox Publisher] Critical error: {e}")
            await asyncio.sleep(5)
        
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(publish_unpublished_events())
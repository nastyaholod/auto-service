from pydantic_settings import BaseSettings

class DatabaseConfig(BaseSettings):
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    database: str = "billing_service"

    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    model_config = {"env_prefix": "BILLING_DB_"}

class RabbitMQConfig(BaseSettings):
    host: str = "localhost"
    port: int = 5672
    user: str = "guest"
    password: str = "guest"

    @property
    def dsn(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}//"

    model_config = {"env_prefix": "RABBITMQ_"}
from sqlalchemy import String, Integer, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid import UUID

class Base(DeclarativeBase):
    pass

class SparePartModel(Base):
    __tablename__ = "spare_parts"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    article_number: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    price_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    stock_quantity: Mapped[int] = mapped_column(Integer)
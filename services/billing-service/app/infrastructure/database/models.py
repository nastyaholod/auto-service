from sqlalchemy import String, Numeric, DateTime, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid import UUID
from datetime import datetime
import enum

class Base(DeclarativeBase):
    pass

class InvoiceStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"

class InvoiceModel(Base):
    __tablename__ = "invoices"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    work_order_id: Mapped[UUID] = mapped_column(unique=True, index=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    status: Mapped[InvoiceStatusEnum] = mapped_column(SQLEnum(InvoiceStatusEnum), default=InvoiceStatusEnum.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
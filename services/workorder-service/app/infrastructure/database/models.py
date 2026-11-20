from sqlalchemy import String, Integer, Numeric, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from uuid import UUID
from datetime import datetime
import enum

class Base(DeclarativeBase):
    pass

class WorkOrderStatusEnum(str, enum.Enum):
    DRAFT = "DRAFT"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CLOSED = "CLOSED"

class WorkOrderModel(Base):
    __tablename__ = "work_orders"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    vehicle_id: Mapped[UUID] = mapped_column(index=True)
    status: Mapped[WorkOrderStatusEnum] = mapped_column(SQLEnum(WorkOrderStatusEnum))
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    lines: Mapped[list["WorkOrderLineModel"]] = relationship(back_populates="work_order", cascade="all, delete-orphan")

class WorkOrderLineModel(Base):
    __tablename__ = "work_order_lines"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    work_order_id: Mapped[UUID] = mapped_column(ForeignKey("work_orders.id"))
    part_id: Mapped[UUID] = mapped_column(index=True)
    part_name: Mapped[str] = mapped_column(String(200))
    quantity: Mapped[int] = mapped_column(Integer)
    price_at_moment: Mapped[float] = mapped_column(Numeric(10, 2))
    
    work_order: Mapped["WorkOrderModel"] = relationship(back_populates="lines")

class OutboxEventModel(Base):
    __tablename__ = "outbox_events"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    event_type: Mapped[str] = mapped_column(String(100))
    payload: Mapped[str] = mapped_column(String(10000))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    published: Mapped[bool] = mapped_column(default=False)
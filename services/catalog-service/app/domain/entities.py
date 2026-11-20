from dataclasses import dataclass, field
from uuid import UUID, uuid4
from app.domain.value_objects import Money

@dataclass
class SparePart:
    id: UUID
    article_number: str
    name: str
    price: Money
    stock_quantity: int

    @classmethod
    def create(cls, article_number: str, name: str, price_amount: float, stock_quantity: int) -> "SparePart":
        return cls(
            id=uuid4(),
            article_number=article_number.upper(),
            name=name,
            price=Money(amount=price_amount),
            stock_quantity=stock_quantity
        )
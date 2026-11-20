from pydantic import BaseModel, Field
from uuid import UUID

class CreateSparePartCommand(BaseModel):
    article_number: str = Field(min_length=3, max_length=50)
    name: str = Field(min_length=2, max_length=200)
    price_amount: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)

class SparePartDTO(BaseModel):
    id: UUID
    article_number: str
    name: str
    price_amount: float
    currency: str
    stock_quantity: int
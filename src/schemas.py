from models import Category
from pydantic import BaseModel, Field


class ProductIn(BaseModel):
    name: str
    description: str | None = None
    category: Category
    quantity: int = Field(default=0, ge=0)
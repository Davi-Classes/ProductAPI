from models import Category
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class MessageOut(BaseModel):
    message: str


class ProductIn(BaseModel):
    name: str
    description: str | None = None
    category: Category
    quantity: int = Field(default=0, ge=0)


class ProductOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    quantity: int
    category: Category
    created_at: datetime 

    model_config: ConfigDict = ConfigDict(from_attributes=True)
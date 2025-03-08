from enum import StrEnum
from datetime import datetime, timezone

from db import Long, BaseModel
from sqlalchemy import Column, String, Integer, DateTime, Enum
from sqlalchemy.orm import Mapped


class Category(StrEnum):
    FOOD = 'ALIMENTO'
    CLEANING = 'LIMPEZA'
    HYGIENE = 'HIGIENE'
    ELETRONIC = 'ELETRONICO'


class Product(BaseModel):
    __tablename__ = 'products'

    id: Mapped[int] = Column(Long, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String(255), nullable=False)
    description: Mapped[str] = Column(String(255), nullable=True)
    quantity: Mapped[int] = Column(Integer, nullable=False, default=0)
    category: Mapped[Category] = Column(type_=Enum(Category), nullable=False)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))

    def __init__(self, name: str, quantity: int, category: Category, description: str | None = None):
        self.name = name
        self.quantity = quantity
        self.category = category
        self.description = description

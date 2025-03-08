from fastapi import FastAPI, Depends
from models import Product
from db import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas import ProductIn, ProductOut, MessageOut


app = FastAPI(title='Product API')


@app.get('/products')
def find_all_products(
    db: Session = Depends(get_db)
) -> list[ProductOut]:
    query = select(Product)

    products = db.execute(query).scalars().all()

    return products

@app.post('/products')
def create_product(
    product_in: ProductIn,
    db: Session = Depends(get_db)
) -> MessageOut:
    data = product_in.model_dump()
    product = Product(**data)
    
    db.add(product)
    db.commit()

    return MessageOut(message='Produto cadastrado com sucesso.')
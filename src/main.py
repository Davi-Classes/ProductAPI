from fastapi import FastAPI, Depends, HTTPException, status
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

@app.get('/products/{id}')
def find_product_by_id(id: int, db: Session = Depends(get_db)) -> ProductOut:
    query = select(Product).where(Product.id == id)
    product = db.execute(query).scalars().first()

    if product is None:
        raise HTTPException(
            detail='Produto não encontrado.',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    return product

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

@app.put('/products/{id}')
def update_product_by_id(
    id: int,
    product_in: ProductIn,
    db: Session = Depends(get_db)
) -> MessageOut:
    query = select(Product).where(Product.id == id)
    product = db.execute(query).scalars().first()

    if product is None:
        raise HTTPException(
            detail='Produto não encontrado.',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    data = product_in.model_dump()
    product.update(**data)
    db.commit()

    return MessageOut(message='Produto atualizado com sucesso.')


@app.delete('/products/{id}')
def delete_product_by_id(
    id: int, 
    db: Session = Depends(get_db)
) -> MessageOut:
    query = select(Product).where(Product.id == id)
    product = db.execute(query).scalars().first()

    if product is None:
        raise HTTPException(
            detail='Produto não encontrado.',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    db.delete(product)
    db.commit()

    return MessageOut(message='Produto excluído com sucesso.')
import db
from fastapi import FastAPI, HTTPException, status
from models import Category, Product
from schemas import MessageOut, ProductIn, ProductOut


app = FastAPI(title='Product API')


@app.get('/products')
def find_all_products(
    category: Category | None = None
) -> list[ProductOut]:
    products = db.get_all_products(category)

    if len(products) == 0:
        raise HTTPException(status.HTTP_204_NO_CONTENT)

    return products


@app.get('/products/{id}')
def find_product_by_id(id: int) -> ProductOut:
    product = db.get_product_by_id(id)

    if product is None:
        raise HTTPException(
            detail='Produto não encontrado.',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    return product


@app.post('/products', status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductIn) -> MessageOut:
    product = db.get_product_by_name_and_category(
        name=product_in.name, 
        category=product_in.category
    )
    
    if product is not None:
        raise HTTPException(
            detail='Já existe um produto com esse nome dessa categoria',
            status_code=status.HTTP_400_BAD_REQUEST
        )

    data = product_in.model_dump()
    product = Product(**data)
    db.create_new_product(product)
    return MessageOut(message='Produto cadastrado com sucesso.')


@app.put('/products/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_product(id: int, product_in: ProductIn) -> MessageOut:
    product = db.get_product_by_id(id)

    if product is None:
        raise HTTPException(
            detail='Produto não encontrado.',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    exists_product = db.get_product_by_name_and_category(
        name=product_in.name, 
        category=product_in.category
    )
    
    if exists_product is not None and product.id != exists_product.id:
        raise HTTPException(
            detail='Já existe um produto com esse nome dessa categoria',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    product.name = product_in.name
    product.description = product_in.description
    product.category = product_in.category
    product.quantity = product_in.quantity

    db.update_product(product)
    return MessageOut(message='Produto atualizado com sucesso.')


@app.delete('/products/{id}', status_code=status.HTTP_202_ACCEPTED)
def delete_product(id: int):
    product = db.get_product_by_id(id)

    if product is None:
        raise HTTPException(
            detail='Produto não encontrado.',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    db.delete_product(id)
    return MessageOut(message='Produto excluído com sucesso.')

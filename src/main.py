from fastapi import FastAPI
from models import Product
from schemas import ProductIn


products = []
app = FastAPI(title='Product API')


@app.get('/products')
def find_all_products():
    return products

@app.post('/products')
def create_product(product_in: ProductIn):
    data = product_in.model_dump()
    product = Product(**data)
    
    # Mesma coisa que estamos fazendo acima
    # product = Product(
    #     name=product_in.name, 
    #     description=product_in.description,
    #     category=product_in.category,
    #     quantity=product_in.quantity
    # )
    
    products.append(product)
    return product
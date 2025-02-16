from models import Category, Product
from tinydb import TinyDB, Query


db = TinyDB('./database.json', indent=2)


def get_all_products(
    category: Category | None = None
) -> list[Product]:
    if category is None:
        results = db.table('products').all()
    else:
        results = db.table('products').search(Query().category == category)

    return results


def get_product_by_id(id: int) -> Product | None:
    product = db.table('products').get(doc_id=id)
    return Product(id=id, **product) if product is not None else None


def get_product_by_name_and_category(
    name: str, category: Category
) -> Product | None:
    result = db.table('products')\
        .search(Query().name == name and Query().category == category)
    
    if len(result) == 0:
        return None
    
    return Product(**result[0])


def create_new_product(product: Product) -> Product:
    product_document = product.model_dump()
    product_document.update({
        'created_at': product.created_at.isoformat()
    })
    product.id = db.table('products').insert(product_document)
    return product


def update_product(product: Product) -> Product:
    product_document = product.model_dump()
    product_document.update({
        'created_at': product.created_at.isoformat()
    })

    product.id = db.table('products')\
        .update(product_document, doc_ids=[product.id])
    return product


def delete_product(id: int):
    db.table('products').remove(doc_ids=[id])
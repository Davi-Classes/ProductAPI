from db import BaseModel, engine
from models import Product


BaseModel.metadata.create_all(bind=engine)

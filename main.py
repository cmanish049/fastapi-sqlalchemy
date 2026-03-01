from fastapi import FastAPI, Depends
from typing_extensions import Annotated
from sqlalchemy.orm import Session

from schemas.models import Product as ProductSchema
from db.databse import get_db, Base, engine
from models.models import Product as ProductModel

app = FastAPI()

Base.metadata.create_all(bind=engine)

products = [
    ProductSchema(id=1, name="Laptop", description="A high-performance laptop", price=999.99, quantity=10),
    ProductSchema(id=2, name="Smartphone", description="A latest model smartphone", price=499.99, quantity=20),
    ProductSchema(id=3, name="Headphones", description="Noise-cancelling headphones", price=199.99, quantity=15),
    ProductSchema(id=4, name="Smartwatch", description="A smartwatch with various features", price=299.99, quantity=5),
]

def init_db():
    db = next(get_db())
    count = db.query(ProductModel).count()
    if count == 0:
        for product in products:
            db.add(ProductModel(**product.model_dump()))
        db.commit()

init_db()

dbDependency = Annotated[Session, Depends(get_db)]

@app.get("/")
def home():
    return {"message" : "Hello World"}

@app.get('/products')
def get_products(db: dbDependency):
    return db.query(ProductModel).all()

@app.get('/products/{product_id}')
def get_product(product_id: int, db: dbDependency):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product:
        return product
    return {"message": "Product not found"}

@app.post('/products')
def add_product(product: ProductSchema, db: dbDependency):
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {"message": "Product added successfully", "product": db_product}

@app.put('/products/{product_id}')
def update_product(product_id: int, updated_product: ProductSchema, db: dbDependency):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product:
        for key, value in updated_product.model_dump().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return {"message": "Product updated successfully", "product": db_product}
    return {"message": "Product not found"}

@app.delete('/products/{product_id}')
def delete_product(product_id: int, db: dbDependency):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted successfully"}
    return {"message": "Product not found"}
from fastapi import FastAPI
from routers import user ,product,order,seller,cart # Adjust the import based on your structure
from . import database

app = FastAPI()

# Initialize the database
database.init_db()

# Include user router
app.include_router(user.router)

app.include_router(seller.router)

app.include_router(product.router)

app.include_router(order.router)

app.include_router(cart.router)

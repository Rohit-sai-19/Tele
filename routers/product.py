from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.orm import Session
from tele import schemas, models, oauth2
from repository import product  
from tele.database import get_db
from typing import List

# Initialize the router for Product operations
router = APIRouter(tags=["Product"], prefix='/products')

# desc: Route to create and store a new product
# method: POST
# return: Stores the product details in the database
@router.post("/create", response_model=schemas.Create_Product, status_code=status.HTTP_201_CREATED)
def create_product(
    request: schemas.Create_Product,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_seller)  # Ensure the current user is a seller
):
    return product.create_product(request, db, current_user)

# desc: Route to update an existing product
# method: PUT
# return: Updates the product details in the database
@router.put("/update/{product_id}", response_model=schemas.Create_Product)
def update_product(
    product_id: int,
    request: schemas.Create_Product = Body(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_seller)  # Ensure the current user is a seller
):
    return product.update_product(product_id, request, db, current_user)

# desc: Route to delete a product
# method: DELETE
# return: Deletes the product from the database
@router.delete("/delete/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.get_current_seller)  # Ensure the current user is a seller
):
    return product.delete_product(product_id, db, current_user)

# desc: Route to get details of a single product
# method: GET
# return: Retrieves product details
@router.get("/{product_id}", response_model=schemas.Create_Product)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return product.get_product(product_id, db)

# desc: Route to get a list of all products
# method: GET
# return: Retrieves a list of all products
@router.get("", response_model=List[schemas.Create_Product])
def get_all_products(db: Session = Depends(get_db)):
    return product.get_all_products(db)

# desc: Route to get products by their name
# method: GET
# return: Retrieves a list of products that match the given name
@router.get("/get/{product_name}", response_model=List[schemas.Create_Product])
def get_product_by_name(
    product_name: str,
    db: Session = Depends(get_db)
):
    return product.get_product_by_name(product_name, db)

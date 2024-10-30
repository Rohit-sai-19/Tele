from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from tele import schemas, database, oauth2,models
from repository import cart
from typing import List,Dict

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)

get_db = database.get_db

# desc: Setting the route to add new items to the cart
# method: POST
# return: Adds items to cart and returns the cart item details
@router.post("/add", response_model=schemas.Cart)
def add_item_to_cart(
    request: schemas.CartCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    return cart.add_to_cart(request, user_id=current_user.user_id, db=db)

# desc: Setting the route to get all items in the user's cart
# method: GET
# return: Returns all items in the user's cart along with the total price
@router.get("/items", response_model=schemas.CartResponse)
def read_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    return cart.get_cart_items(current_user.user_id, db)

# desc: Setting the route to update an item in the cart
# method: PUT
# return: Updates the quantity of the specified cart item and returns the updated cart item details
@router.put("/update/{cart_id}", response_model=schemas.Cart)
def update_cart_item(
    cart_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    return cart.update_cart_item(cart_id=cart_id, quantity=quantity, user_id=current_user.user_id, db=db)

# desc: Setting the route to delete an item from the cart
# method: DELETE
# return: Deletes the specified cart item
@router.delete("/delete/{cart_id}")
def delete_cart_item(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    return cart.delete_cart_item(cart_id=cart_id, user_id=current_user.user_id, db=db)

# desc: Setting the route to calculate the total price of items in the cart
# method: GET
# return: Returns the total price of all items in the user's cart
@router.get("/total")
def calculate_total(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    return cart.calculate_cart_total(user_id=current_user.user_id, db=db)

# desc: Setting the route to order all items in the cart
# method: POST
# return: Places an order for all items in the user's cart
@router.post("/order")
def order_all_cart_items(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    return cart.order_cart(user_id=current_user.user_id, db=db)
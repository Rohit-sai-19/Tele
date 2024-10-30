from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from tele import schemas, database, oauth2
from repository import order

# Initialize the router for Order operations
router = APIRouter(tags=["Orders"], prefix='/orders')

# desc: Route to create a new order
# method: POST
# return: Creates a new order and returns the order response
@router.post("/all", response_model=schemas.OrderResponse)
def create_order(
    request: schemas.OrderCreate, 
    db: Session = Depends(database.get_db), 
    current_user: schemas.Create_User = Depends(oauth2.get_current_user)  # Ensure the current user is authenticated
):
    return order.create_order(request, current_user.user_id, db)

# desc: Route to get details of a specific order by ID
# method: GET
# return: Retrieves order details for the given order ID
@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(database.get_db)
):
    return order.get_order_by_id(order_id, db)

# desc: Route to update an existing order
# method: PUT
# return: Updates the order details and returns the updated order response
@router.put("/update/{order_id}", response_model=schemas.OrderResponse)
def update_order(
    order_id: int, 
    request: schemas.OrderUpdate, 
    db: Session = Depends(database.get_db)
):
    return order.update_order(order_id, request, db)

# desc: Route to delete an existing order
# method: DELETE
# return: Deletes the specified order
@router.delete("/delete/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(database.get_db)
):
    return order.delete_order(order_id, db)

# desc: Route to process payment for an existing order
# method: PUT
# return: Updates the order to mark it as paid and returns the updated order response
@router.put("/pay/{order_id}", response_model=schemas.OrderResponse)
def pay_order(
    order_id: int, 
    request: schemas.OrderUpdate, 
    db: Session = Depends(database.get_db)
):
    return order.pay_order(order_id, request, db)

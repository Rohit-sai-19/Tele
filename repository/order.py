from sqlalchemy.orm import Session
from tele import models, schemas
from fastapi import HTTPException, status
import random
import string
from datetime import datetime, timedelta


# desc: Generate a random string of characters for the tracking number
def generate_tracking_number(length: int = 10) -> str:
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# desc: Generate the estimated delivery date (one week from the current date)
def get_estimated_delivery_date() -> str:
    return (datetime.now() + timedelta(weeks=1)).date()


# desc: Create a new order in the database
# params: request (OrderCreate schema), user_id (int), db (Session)
# return: Newly created order object
def create_order(request: schemas.OrderCreate, user_id: int, db: Session):
    # Fetch the product to get the price and stock
    product = db.query(models.Product).filter(models.Product.product_id == request.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if there is enough stock for the order
    if product.stock < request.quantity:
        raise HTTPException(status_code=400, detail="Out of stock")

    # Fetch the user to get the delivery address
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Calculate the total price based on quantity
    total_price = product.discounted_price * request.quantity

    # Generate a random tracking number
    tracking_number = generate_tracking_number()

    # Get the estimated delivery date
    estimated_delivery_date = get_estimated_delivery_date()

    new_order = models.Order(
        user_id=user_id,
        product_id=request.product_id,
        quantity=request.quantity,
        total_price=total_price,
        delivery_address=user.address,
        payment_method=request.payment_method,
        tracking_number=tracking_number,
        estimated_delivery_date=estimated_delivery_date
    )

    # Decrease the product stock
    product.stock -= request.quantity

    # Add and commit the new order to the database
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    db.refresh(product)

    return new_order


# desc: Retrieve an order by its ID
# params: order_id (int), db (Session)
# return: Order object if found, else raises HTTPException
def get_order_by_id(order_id: int, db: Session):
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


# desc: Update an existing order
# params: order_id (int), request (OrderUpdate schema), db (Session)
# return: Updated order object
def update_order(order_id: int, request: schemas.OrderUpdate, db: Session):
    order = get_order_by_id(order_id, db)

    if request.order_status is not None:
        order.order_status = request.order_status
    if request.payment_status is not None:
        order.payment_status = request.payment_status
    if request.tracking_number is not None:
        order.tracking_number = request.tracking_number
    if request.estimated_delivery_date is not None:
        order.estimated_delivery_date = request.estimated_delivery_date

    db.commit()
    db.refresh(order)
    return order


# desc: Delete an order by its ID
# params: order_id (int), db (Session)
# return: Confirmation message and deleted order details
def delete_order(order_id: int, db: Session):
    order = get_order_by_id(order_id, db)

    db.delete(order)
    db.commit()
    return {"detail": "Order deleted successfully", "order": order}


# desc: Mark an order as paid
# params: order_id (int), request (OrderUpdate schema), db (Session)
# return: Updated order object
def pay_order(order_id: int, request: schemas.OrderUpdate, db: Session):
    order = get_order_by_id(order_id, db)

    # Update payment status to "paid"
    order.payment_status = "paid"

    # Update other fields if provided in the request
    if request.order_status is not None:
        order.order_status = request.order_status
    if request.tracking_number is not None:
        order.tracking_number = request.tracking_number
    if request.estimated_delivery_date is not None:
        order.estimated_delivery_date = request.estimated_delivery_date

    db.commit()
    db.refresh(order)
    return order

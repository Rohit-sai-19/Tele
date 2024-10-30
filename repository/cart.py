from fastapi import HTTPException
from sqlalchemy.orm import Session
from tele import schemas, models
import random
import string
from datetime import datetime, timedelta

# Function to generate a unique tracking number
def generate_tracking_number(length: int = 10) -> str:
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Function to calculate the estimated delivery date (1 week from now)
def get_estimated_delivery_date() -> str:
    return (datetime.now() + timedelta(weeks=1)).date()

# Function to calculate the total price of items in the user's cart
def calculate_cart_total(user_id: int, db: Session):
    cart_items = db.query(models.Cart).filter(models.Cart.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")
    
    total = sum(item.quantity * db.query(models.Product).filter(models.Product.product_id == item.product_id).first().discounted_price for item in cart_items)
    return {"total_price": total}

# desc: Adds a new item to the user's cart or updates the quantity if it already exists
# method: POST
# return: The cart item details after adding/updating
def add_to_cart(request: schemas.CartCreate, user_id: int, db: Session):
    product = db.query(models.Product).filter(models.Product.product_id == request.product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock < request.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock for this quantity")
    
    cart_item = db.query(models.Cart).filter(
        models.Cart.user_id == user_id,
        models.Cart.product_id == request.product_id
    ).first()

    if cart_item:
        cart_item.quantity += request.quantity
    else:
        cart_item = models.Cart(
            user_id=user_id,
            product_id=request.product_id,
            quantity=request.quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item

# desc: Retrieves all items in the user's cart along with their details and total price
# method: GET
# return: A dictionary containing the total price and item details
def get_cart_items(user_id: int, db: Session):
    cart_items = db.query(models.Cart).filter(models.Cart.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")

    total_price = 0.0
    items_with_details = []

    for item in cart_items:
        product = db.query(models.Product).filter(models.Product.product_id == item.product_id).first()
        if product:
            item_total = product.discounted_price * item.quantity
            total_price += item_total

            items_with_details.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "item_total": item_total,
                "product_name": product.product_name,
                "product_price": product.discounted_price
            })

    return {
        "total_price": total_price,
        "items": items_with_details
    }

# desc: Updates the quantity of a specific item in the user's cart
# method: PUT
# return: The updated cart item details
def update_cart_item(cart_id: int, quantity: int, user_id: int, db: Session):
    cart_item = db.query(models.Cart).filter(models.Cart.cart_id == cart_id, models.Cart.user_id == user_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    product = db.query(models.Product).filter(models.Product.product_id == cart_item.product_id).first()
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock for this quantity")
    
    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

# desc: Deletes an item from the user's cart
# method: DELETE
# return: A success message indicating the item has been deleted
def delete_cart_item(cart_id: int, user_id: int, db: Session):
    cart_item = db.query(models.Cart).filter(models.Cart.cart_id == cart_id, models.Cart.user_id == user_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return {"detail": "Item deleted from cart"}

# desc: Processes an order for all items in the user's cart
# method: POST
# return: A summary of the order, including the total cost and order details
def order_cart(user_id: int, db: Session):
    cart_items = db.query(models.Cart).filter(models.Cart.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")

    total_order_cost = 0
    order_records = []
    
    for item in cart_items:
        product = db.query(models.Product).filter(models.Product.product_id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")
        
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product ID {product.product_id}")
        
        item_total = product.discounted_price * item.quantity
        total_order_cost += item_total

        product.stock -= item.quantity

        new_order = models.Order(
            user_id=user_id,
            product_id=item.product_id,
            quantity=item.quantity,
            total_price=item_total,
            delivery_address=db.query(models.User).filter(models.User.user_id == user_id).first().address,
            payment_method="Cart Payment",
            tracking_number=generate_tracking_number(),
            estimated_delivery_date=get_estimated_delivery_date()
        )
        db.add(new_order)
        order_records.append(new_order)

    db.commit()
    
    # Serialize orders before returning
    orders_response = [schemas.OrderResponse.from_orm(order) for order in order_records]

    # Clear the cart after successful ordering
    db.query(models.Cart).filter(models.Cart.user_id == user_id).delete()
    db.commit()

    return {"total_order_cost": total_order_cost, "orders": orders_response}

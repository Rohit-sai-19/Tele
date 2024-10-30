from fastapi import HTTPException, status,Depends
from sqlalchemy.orm import Session
from tele import schemas, models,database,jwt_token
from tele.hashing import Hash



current_seller_id = 89 
# desc:for creating the user_id
def generate_seller_id() -> str:
    global current_seller_id
    seller_id = str(current_seller_id).zfill(3)  
    current_seller_id += 1  
    return seller_id 


def create_seller(request: schemas.seller_User, db: Session):
    seller_id = generate_seller_id()
    new_user = models.seller(
        seller_id=seller_id,
        seller_name=request.seller_name,
        phone_number=request.phone_number,
        email_id=request.email_id,
        address=request.address,
        password=Hash.bcrypt(request.password) , 
        gstin_number = request.gstin_number
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login(request: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    seller = db.query(models.seller).filter(models.seller.email_id == request.email_id).first()

    # If user is not found
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    # Verify hashed password
    if not Hash.verify(seller.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")
    
    # Create JWT token
    access_token = jwt_token.create_access_token(data={"sub": seller.email_id})
    
    # Return token and token type
    return {"access_token": access_token, "token_type": "bearer"}

from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from tele import schemas, models, database, jwt_token
from tele.hashing import Hash


current_seller_id = 89


# desc: Generate a unique seller ID, formatted as a three-digit string
# return: Formatted seller ID
def generate_seller_id() -> str:
    global current_seller_id
    seller_id = str(current_seller_id).zfill(3)  # Zero-pad the seller ID to three digits
    current_seller_id += 1  # Increment the seller ID for the next seller
    return seller_id


# desc: Create a new seller in the database
# params: request (seller_User schema), db (Session)
# return: Newly created seller object
def create_seller(request: schemas.seller_User, db: Session):
    seller_id = generate_seller_id()  # Generate a new seller ID
    new_user = models.seller(
        seller_id=seller_id,
        seller_name=request.seller_name,
        phone_number=request.phone_number,
        email_id=request.email_id,
        address=request.address,
        password=Hash.bcrypt(request.password),  # Hash the password before storing
        gstin_number=request.gstin_number
    )
    db.add(new_user)  # Add the new seller to the session
    db.commit()  # Commit the changes to the database
    db.refresh(new_user)  # Refresh the instance to get the latest data
    return new_user


# desc: Authenticate a seller and create a JWT token
# params: request (LoginRequest schema), db (Session)
# return: Dictionary containing access token and token type
def login(request: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    # Find the seller by email
    seller = db.query(models.seller).filter(models.seller.email_id == request.email_id).first()

    # If seller is not found, raise an error
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    # Verify hashed password
    if not Hash.verify(seller.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")
    
    # Create JWT token for the authenticated seller
    access_token = jwt_token.create_access_token(data={"sub": seller.email_id})
    
    # Return the token and its type
    return {"access_token": access_token, "token_type": "bearer"}


# desc: Retrieve all orders for a specific seller
# params: seller_id (int), db (Session)
# return: List of orders associated with the seller
def get_seller_orders(seller_id: int, db: Session):
    # Join Order and Product tables to get orders for products owned by the seller
    seller_orders = db.query(models.Order).join(models.Product, models.Order.product_id == models.Product.product_id) \
                    .filter(models.Product.seller_id == seller_id).all()

    # If no orders found, raise an error
    if not seller_orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No orders found for this seller")

    return seller_orders


def login(request: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    seller = db.query(models.seller).filter(models.seller.email_id == request.email_id).first()

    # If user is not found
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    # Verify hashed password
    if not Hash.verify(seller.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")
    
    # Create JWT token
    access_token = jwt_token.create_access_token(data={"sub": seller.email_id})
    
    # Return token and token type
    return {"access_token": access_token, "token_type": "bearer"}


def get_seller_orders(seller_id: int, db: Session):
    # Join Order and Product tables to get orders for products owned by the seller
    seller_orders = db.query(models.Order).join(models.Product, models.Order.product_id == models.Product.product_id) \
                    .filter(models.Product.seller_id == seller_id).all()

    if not seller_orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No orders found for this seller")

    return seller_orders
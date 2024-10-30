from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from tele import schemas, models, database, jwt_token
from tele.hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm


current_user_id = 3  # Initialize a global user ID counter

# desc: Generate a unique user ID, formatted as a three-digit string
# return: Formatted user ID
def generate_user_id() -> str:
    global current_user_id
    user_id = str(current_user_id).zfill(3)  # Zero-pad the user ID to three digits
    current_user_id += 1  # Increment the user ID for the next user
    return user_id

# desc: Create a new user in the database
# methods: POST
# return: Store the user details in the database
def create_user(request: schemas.Create_User, db: Session):
    user_id = generate_user_id()  # Generate a new user ID
    new_user = models.User(
        user_id=user_id,
        user_name=request.user_name,
        phone_number=request.phone_number,
        email_id=request.email_id,
        address=request.address,
        password=Hash.bcrypt(request.password)  # Hash the password before storing
    )
    db.add(new_user)  # Add the new user to the session
    db.commit()  # Commit the changes to the database
    db.refresh(new_user)  # Refresh the instance to get the latest data
    return new_user

# desc: Retrieve all users from the database
# methods: GET
# return: List of all users in the database
def get_all_users(db: Session):
    employees = db.query(models.User).all()  # Query all users
    return employees

# desc: Update user information in the database
# methods: POST
# return: Updates the details of the user in the database
def update_user_account(
    request: schemas.UpdateUser, 
    current_user: models.User, 
    db: Session
):
    # Update fields only if provided and not equal to the default value
    if request.user_name and request.user_name != "string":
        current_user.user_name = request.user_name
    if request.phone_number and request.phone_number != "string":
        current_user.phone_number = request.phone_number
    if request.email_id and request.email_id != "string":
        current_user.email_id = request.email_id
    if request.address and request.address != "string":
        current_user.address = request.address

    # Commit the changes to the database
    db.commit()
    db.refresh(current_user)  # Refresh to get updated user data
    return current_user

# desc: Authenticate a user and create a JWT token
# methods: POST
# return: Access token for the user
def login(request: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email_id == request.email_id).first()

    # If user is not found, raise an error
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    # Verify hashed password
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")
    
    # Create JWT token for the authenticated user
    access_token = jwt_token.create_access_token(data={"sub": user.email_id})
    
    # Return the token and its type
    return {"access_token": access_token, "token_type": "bearer"}

# desc: Delete a user from the database
# methods: DELETE
# return: Deletes the user from the database
def delete_emp(id: int, db: Session):
    del_emp = db.query(models.User).filter(models.User.user_id == id).first()  # Find user by ID
    if not del_emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {id} not found"  # Raise an error if not found
        )
    db.delete(del_emp)  # Delete the user
    db.commit()  # Commit the changes to the database

# desc: Authenticate user and provide access to protected routes in Swagger UI
# methods: POST
# return: Unlock all routes behind authentication
def login_all(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email_id == request.username).first()  # Find user by email
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    access_token = jwt_token.create_access_token(data={"sub": user.email_id})
    
    # Return the token and its type
    return {"access_token": access_token, "token_type": "bearer"}

# desc: Retrieve the current user's details from the database
# methods: GET
# return: Current user details
def get_users(current_user: models.User, db: Session):
    print("Current user:", current_user)  # Print current user for debugging
    return current_user  # Return the current user details

# desc: Update the user's password
# methods: PUT
# return: Success message upon password update
def update_password(
    request: schemas.PasswordReset, 
    current_user: models.User, 
    db: Session
):
    # Check if the user_id and email_id from the current user match the ones provided in the request
    if request.user_id != current_user.user_id or request.email_id != current_user.email_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID or Email ID does not match."  # Raise an error if IDs do not match
        )

    # Only update if the password field is provided and is not the default value
    if request.password and request.password != "string":
        hashed_password = Hash.bcrypt(request.password)  # Hash the new password before saving
        current_user.password = hashed_password
    
    # Commit the changes to the database
    db.commit()
    db.refresh(current_user)  # Refresh to get updated user data
    
    return {"message": "Password updated successfully!"}  # Return success message

# desc: Retrieve all orders for a specific user
# methods: GET
# return: List of all orders by the user
def get_user_orders(user_id: int, db: Session):
    # Query the Order table to get all orders by the user
    user_orders = db.query(models.Order).filter(models.Order.user_id == user_id).all()

    if not user_orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")  # Raise an error if no orders found

    return user_orders  # Return the list of user orders

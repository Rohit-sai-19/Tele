from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import jwt_token, database, models
from tele.jwt_token import verify_token

oauth2_user_scheme = OAuth2PasswordBearer(tokenUrl="/user/login/all")



# Get the current user based on the JWT token
def get_current_user(token: str = Depends(oauth2_user_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify the token and get the user data
    user_data = verify_token(token)  # Assuming this returns an instance of TokenData

    # Query the database for the user using the email
    user = db.query(models.User).filter(models.User.email_id == user_data.email).first()

    if user is None:
        raise credentials_exception

    return user

oauth2_seller_scheme = OAuth2PasswordBearer(tokenUrl="/products/login/all")



# Get the current user based on the JWT token
def get_current_seller(token: str = Depends(oauth2_seller_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify the token and get the user data
    user_data = verify_token(token)  # Assuming this returns an instance of TokenData

    # Query the database for the user using the email
    user = db.query(models.seller).filter(models.seller.email_id == user_data.email).first()

    if user is None:
        raise credentials_exception

    return user



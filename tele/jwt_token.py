from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
import os
import logging
from tele import schemas

# Constants for JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Set up logging
logger = logging.getLogger(__name__)

# Create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify JWT token and extract user information
def verify_token(token: str) -> schemas.TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        current_user = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = current_user.get("sub")  # JWT uses 'sub' to store the subject (email)
        if email is None:
            raise credentials_exception
        return schemas.TokenData(email= email)  # Return email inside TokenData
    except JWTError as e:
        logger.error(f"Token verification failed: {e}")
        raise credentials_exception

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import date,datetime
from typing import List

class Create_User(BaseModel):
    user_id: int
    user_name: str
    phone_number: str
    email_id: EmailStr
    address: str
    password :str

    class Config:
        from_attributes = True  

class UpdateUser(BaseModel):
    user_name: Optional[str] = None
    phone_number: Optional[str] = None
    email_id: Optional[str] = None
    address: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str



class TokenData(BaseModel):
    email: Optional[str] = None
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email_id: str
    password: str



class PasswordReset(BaseModel):
    user_id: int
    email_id: str
    password: str


class seller_User(BaseModel):
    seller_id: int
    seller_name: str
    phone_number: str
    email_id: EmailStr
    address: str
    password :str
    gstin_number : str
    
    class Config:
        from_attributes = True  

class Create_Product(BaseModel):
    product_id: int
    product_name: str
    description: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    price: float
    discount: Optional[float] = Field(default=0.0, description="Discount percentage")
    discounted_price : Optional[float] = None
    stock: int
    sku: str
    image_url: Optional[str] = None
    rating: Optional[float] = Field(default=0.0, description="Rating out of 5")
    reviews_count: Optional[int] = Field(default=0, description="Number of reviews")
    launch_date: Optional[date] = None
    color: Optional[str] = None
    size: Optional[str] = None
    dimensions: Optional[str] = None
    weight: Optional[float] = None
    seller_id: int  # Foreign key linking to the User table (Seller)
    shipping_info: Optional[str] = None
    return_policy: Optional[str] = None
    warranty: Optional[str] = None
    product_status: Optional[str] = Field(default='available', description="Status of the product")
    featured: Optional[bool] = Field(default=False, description="Whether the product is featured")
    tax: Optional[float] = Field(default=0.0, description="Tax percentage")
    product_video: Optional[str] = None
    tags: Optional[str] = None

    class Config:
        from_attributes = True



class OrderBase(BaseModel):
    product_id: int
    quantity: int
    total_price: float
    delivery_address: Optional[str]
    payment_method: str

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    order_status: Optional[str] = None
    payment_status: Optional[str] = None
    tracking_number: Optional[str] = None
    estimated_delivery_date: Optional[datetime] = None

class OrderResponse(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    total_price: float
    order_status: str
    order_date: datetime
    delivery_address: str
    payment_method: str
    payment_status: str
    tracking_number: str = None
    estimated_delivery_date: datetime = None

    class Config:
        from_attributes = True

    # Validator to format the order_date
    @validator('order_date', pre=True, always=True)
    def format_order_date(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return value

    # Validator to format the estimated_delivery_date
    @validator('estimated_delivery_date', pre=True, always=True)
    def format_estimated_delivery_date(cls, value):
        if value and isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return value
    

class CartItem(BaseModel):
    product_id: int
    quantity: int
    item_total: float
    product_name: str
    product_price: float

class CartResponse(BaseModel):
    total_price: float
    items: List[CartItem]

class CartCreate(BaseModel):
    product_id: int
    quantity: int

class Cart(BaseModel):
    cart_id: int
    user_id: int
    product_id: int
    quantity: int
    added_date: datetime

    class Config:
        from_attributes = True

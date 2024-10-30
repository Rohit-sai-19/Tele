from sqlalchemy import Column, Integer, String,Float,Boolean,ForeignKey,DateTime
from .database import Base  # Adjusted for relative import
from sqlalchemy.orm import relationship
from datetime import datetime
class User(Base):
    __tablename__ = 'user'
    
    user_id = Column(Integer, unique=True, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)  # Store phone number as string
    email_id = Column(String, unique=True, nullable=False)
    address = Column(String)
    password = Column(String)
    
    # Relationships
    products = relationship("Product", back_populates="seller")
    orders = relationship("Order", back_populates="user")
    cart_items = relationship("Cart", back_populates="user")
class seller(Base):
    __tablename__ = 'seller'
    
    seller_id = Column(Integer, unique=True, primary_key=True, index=True)
    seller_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)  # Store phone number as string
    email_id = Column(String, unique=True, nullable=False)
    address = Column(String)
    password = Column(String)
    gstin_number = Column(String,unique=True, nullable=False)
    # Relationships

class Product(Base):
    __tablename__ = 'product'

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    description = Column(String)
    category = Column(String, nullable=False)
    subcategory = Column(String)
    brand = Column(String)
    price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0) 
    discounted_price = Column(Float)
    stock = Column(Integer, nullable=False)  # Stock available
    sku = Column(String, nullable=False)  # SKU for inventory tracking
    image_url = Column(String)  # URL or path for product image
    rating = Column(Float, default=0.0)  # Product rating
    reviews_count = Column(Integer, default=0)  # Number of reviews
    launch_date = Column(String)  # Date when the product was launched
    color = Column(String)
    size = Column(String)  # Can be size for clothing or dimensions for other products
    dimensions = Column(String)  # e.g., "10x5x3" for physical products
    weight = Column(Float)
    seller_id = Column(Integer, ForeignKey('user.user_id'))  # Reference to User table
    shipping_info = Column(String)  # Shipping details like options, costs
    return_policy = Column(String)  # Return or exchange policy
    warranty = Column(String)  # Warranty details if applicable
    product_status = Column(String, default='available')  # e.g., available, out of stock, discontinued
    featured = Column(Boolean, default=False)  # If the product is featured or promoted
    tax = Column(Float, default=0.0)  # Tax percentage applied
    product_video = Column(String)  # Link to a product video if available
    tags = Column(String)  # Keywords for search optimization

    # Relationships
    seller = relationship("User", back_populates="products")  # Reference to the User table
    orders = relationship("Order", back_populates="product")  # Relationship with orders
    cart_items = relationship("Cart", back_populates="product")
class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))  # Reference to User table
    product_id = Column(Integer, ForeignKey('product.product_id'))  # Reference to Product table
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    order_status = Column(String, default="Pending")
    order_date = Column(DateTime, default=datetime.now)
    delivery_address = Column(String, nullable=False)
    payment_method = Column(String, nullable=False)
    payment_status = Column(String, default="Unpaid")
    tracking_number = Column(String, nullable=True)
    estimated_delivery_date = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="orders")  # Reference to User table
    product = relationship("Product", back_populates="orders")


class Cart(Base):
    __tablename__ = "cart"
    
    cart_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    product_id = Column(Integer, ForeignKey("product.product_id"))
    quantity = Column(Integer, nullable=False)
    added_date = Column(DateTime, default=datetime.now)
    


    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")
 
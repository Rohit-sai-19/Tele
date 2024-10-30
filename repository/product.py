from fastapi import HTTPException, status,Depends
from sqlalchemy.orm import Session
from tele import schemas, models
import random,string
from datetime import datetime

def generate_package_number(length: int = 10) -> str:
    digits = string.digits  # Only digits 0-9
    return ''.join(random.choice(digits) for _ in range(length))

def generate_sku_number(length: int = 8) -> str:
    digits = string.digits  # Only digits 0-9
    return ''.join(random.choice(digits) for _ in range(length))

def discount(price: float, discount_percent: float) -> float:
    if discount_percent <= 0 or discount_percent >= 100:
        return price  
    return price - (price * (discount_percent / 100))

current_seller_id = 86 

def generate_seller_id() -> str:
    global current_seller_id
    user_id = str(current_seller_id).zfill(3)  
    current_seller_id += 1  
    return user_id 
# desc: Create and store a new product in the database
# methods : POST
# return : stores the product details in the database
def create_product(request: schemas.Create_Product, db: Session, current_seller: models.seller):
    # Check if a product with the same SKU already exists
    existing_product = db.query(models.Product).filter(models.Product.sku == request.sku).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product with this SKU already exists")

    # Generate a unique product ID
    product_number = generate_package_number()
    
    sku_number = generate_sku_number()
    
    # Ensure the launch_date is properly formatted
    launch_date = request.launch_date
    
    discounted_price = discount(float(request.price), float(request.discount))

    if isinstance(launch_date, str):
        launch_date = datetime.strptime(launch_date, "%Y-%m-%d").date()

    new_product = models.Product(
        product_id=product_number,
        product_name=request.product_name,
        description=request.description,
        category=request.category,
        subcategory=request.subcategory,
        brand=request.brand,
        price=float(request.price),  
        discount=float(request.discount),  
        discounted_price = float(discounted_price),
        stock=int(request.stock),  
        sku = sku_number,
        image_url=request.image_url,
        rating=float(request.rating),  
        reviews_count=int(request.reviews_count), 
        launch_date=launch_date,  
        color=request.color,
        size=request.size,
        dimensions=request.dimensions,
        weight=float(request.weight), 
        seller_id=current_seller.seller_id,  
        shipping_info=request.shipping_info,
        return_policy=request.return_policy,
        warranty=request.warranty,
        product_status=request.product_status,
        featured=bool(request.featured),  
        tax=float(request.tax), 
        product_video=request.product_video,
        tags=request.tags
    )
    
    # Add and commit the new product to the database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# desc: Get a single product by its ID
# methods : GET
# return : retrieves the product details
def get_product(product_id: int, db: Session):
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

# desc: Retrieve all products from the database
# methods : GET
# return : retrieves a list of all products
def get_all_products(db: Session):
    products = db.query(models.Product).all()
    return products

# desc: Update an existing product
# methods : PUT
# return : updates the product details in the database
def update_product(product_id: int, request: schemas.Create_Product, db: Session, current_seller: models.seller):
    product = db.query(models.Product).filter(models.Product.product_id == product_id, models.Product.seller_id == current_seller.seller_id).first()
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or not authorized to update")
    
    product.product_name = request.product_name or product.product_name
    product.description = request.description or product.description
    product.category = request.category or product.category
    product.subcategory = request.subcategory or product.subcategory
    product.brand = request.brand or product.brand
    product.price = request.price or product.price
    product.discount = request.discount or product.discount
    product.stock = request.stock or product.stock
    product.sku = request.sku or product.sku
    product.image_url = request.image_url or product.image_url
    product.rating = request.rating or product.rating
    product.reviews_count = request.reviews_count or product.reviews_count
    product.launch_date = request.launch_date or product.launch_date
    product.color = request.color or product.color
    product.size = request.size or product.size
    product.dimensions = request.dimensions or product.dimensions
    product.weight = request.weight or product.weight
    product.shipping_info = request.shipping_info or product.shipping_info
    product.return_policy = request.return_policy or product.return_policy
    product.warranty = request.warranty or product.warranty
    product.product_status = request.product_status or product.product_status
    product.featured = request.featured or product.featured
    product.tax = request.tax or product.tax
    product.product_video = request.product_video or product.product_video
    product.tags = request.tags or product.tags

    db.commit()
    db.refresh(product)
    return product

# desc: Delete a product from the database
# methods : DELETE
# return : deletes the product
def delete_product(product_id: int, db: Session, current_user: models.seller):
    product = db.query(models.Product).filter(models.Product.product_id == product_id, models.Product.seller_id == current_user.seller_id).first()
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or not authorized to delete")
    
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}

# desc: search for a product from the database using product name
# methods : get
# return : returns the product
def get_product_by_name(product_name: str, db: Session):
    # Use %product_name% for case-insensitive search
    search_term = f"%{product_name}%"
    product = db.query(models.Product).filter(models.Product.product_name.ilike(search_term)).all()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product
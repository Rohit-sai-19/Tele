from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from tele import schemas, database, models, oauth2
from repository import seller  
from tele.schemas import seller_User
from tele.database import get_db

# Initialize the router for the Seller operations
router = APIRouter(tags=["Seller"], prefix='/Seller')

# desc: Route to register a new seller
# methods: POST
# return: Created seller information
@router.post("/register", response_model=seller_User)
def create_user(request: seller_User, db: Session = Depends(get_db)):
    return seller.create_seller(request, db)

# desc: Route for seller login
# methods: POST
# return: Access token upon successful login
@router.post('/login')
def login(request: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    return seller.login(request, db)

# desc: Route to retrieve orders for the current seller
# methods: GET
# return: List of orders for the current seller
@router.get("/orders/me", response_model=list[schemas.OrderResponse])
def get_my_orders(
    current_seller: models.seller = Depends(oauth2.get_current_seller),  # Get the currently logged-in seller
    db: Session = Depends(database.get_db)
):
    return seller.get_seller_orders(current_seller.seller_id, db)  # Fetch orders for the current seller

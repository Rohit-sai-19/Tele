from fastapi import APIRouter, Depends,status,Body
from sqlalchemy.orm import Session
from tele import schemas,database,models,oauth2
from repository import user
from tele.database import get_db 
from tele.oauth2 import get_current_user
from tele.schemas import Create_User
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/user',tags=["User"],)

# desc:setting the route to get the create and store the user
# methods : POST
#return : store the deatils in the databae
@router.post("/register", response_model= Create_User)
def create_user(request:Create_User ,
                 db: Session = Depends(database.get_db)
                 ):
    return user.create_user(request, db)


# desc:setting the route to get the Acess key for the user
# methods : POST
#return : gets the acess key of the user
@router.post('/login')
def login(request: schemas.LoginRequest,
           db: Session = Depends(database.get_db)
           ):
    return user.login(request, db)


@router.post('/login/all')
def login_all(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    return user.login_all(request,db)

# desc:setting the route to get the update and store the new information of the user
# methods : PUT
#return : updates the deatils in the databae
@router.put('/update/profile', response_model=schemas.UpdateUser)
def update_user_account(
    request: schemas.UpdateUser = Body(...),  # Body is required, but fields are optional
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(oauth2.get_current_user)  # Ensure this returns a User instance
):
    # Call the repository function to update the user account
    updated_user = user.update_user_account(request, current_user, db)
    return updated_user  # Return the updated user object


# desc:setting the route to delete the user
# methods : DELETE
#return : deletes the user from databae
@router.delete('/delete/account', status_code=status.HTTP_204_NO_CONTENT)
def delete_emp(
    db: Session = Depends(get_db),
      current_user: schemas.Create_User = Depends(get_current_user)
      ):
    return user.delete_emp(current_user.user_id, db)

# desc:setting the route to get all the users in the database
# methods : GET
#return : retrive all the user from the databae
@router.get('/all', status_code=status.HTTP_200_OK)
def get_all_employees(db: Session = Depends(get_db)):
    return user.get_all_users(db)



# desc:setting the route to get the the current users data
# methods : GET
#return : retrive the authenticated users data 
@router.get("/about", response_model=schemas.Create_User)
def get_user_data(current_user: models.User = Depends(get_current_user),
                   db: Session = Depends(database.get_db)
                   ):
    return user.get_users(current_user, db)

# desc:setting the route to update the password of the user
# methods : PUT
#return : update the users password
@router.put('/update-password', status_code=status.HTTP_200_OK)
def update_password(
    request: schemas.PasswordReset,  
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user) 
):
    return user.update_password(request, current_user, db)

# desc:setting the route to retrive all the orders done by the uses
# methods : GET
#return : Gets the current user orders
@router.get("/orders/me", response_model=list[schemas.OrderResponse])
def get_my_orders(current_user: models.User = Depends(oauth2.get_current_user),
                   db: Session = Depends(database.get_db)):
    # Get the orders of the current logged-in user
    return user.get_user_orders(current_user.user_id, db)
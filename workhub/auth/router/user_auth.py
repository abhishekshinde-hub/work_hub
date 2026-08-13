
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from workhub.auth.models import User
from workhub.auth.setting import auth_setting
from ..schemas import CreateUser
from workhub.db_connection import get_db

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags = ["User Authentication"])


@router.post("/register")
def user_register(request: CreateUser, db: Session = Depends(get_db)):
    """
    Register a new user in Workhub.

    Args:
        request (CreateUser): User input data.
        db (Session): Database session dependency.

    Returns:
        dict: Success message or error details.

    """
    hashed_password = auth_setting.password_hash(request.password)

    # Password = Password was being handled by argonid method
    user_data = User(
        name=request.name,
        gender=request.gender,
        role=request.role,
        username=request.username,
        password=hashed_password,
        email_id=request.email_id,
        mobile_no=request.mobile_no,
    )

    try:
        db.add(user_data)
        db.commit()
        db.refresh(user_data)
        return {"message": "user registration successfull"}
    except Exception as e:
        raise HTTPException(detail=f"Error: {str(e)}", status_code=400)


def get_user(username, db):
    """
    when we want to check the user weather user is exist or not
    """

    # we are cheking user from db

    get_user_data = db.query(User).filter(User.username == username).first()

    if get_user_data:
       if  get_user_data.is_active:
        return get_user_data
       else : 
          raise HTTPException(detail="User is deactivated", status_code=403)


    # if user not exist then we will have a error
    
    raise HTTPException(detail="Username not found", status_code=404)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    This funtion have login realted logic for login I used jwt and Oauth2
    """
    user_data = get_user(
        form_data.username, db
    )  # get user => that helps us to check we the user exits

    auth_setting.verify_password(
        user_data.password, form_data.password
    )  # decoding userpassword by the verify password funtion

    user_data = {"sub": user_data.username}

    token = auth_setting.create_token(user_data)
    # create token() It taker userdata in string so that it can make sub for token sub always be string value

    return {"access_token": token, "token_type": "bearer"}
@router.post("/forgot_password/{username}")
def forgot_password(username:str,db : Session = Depends(get_db)) :
   user_data = get_user(username, db)
   user_data = {"sub" : user_data.username}
   token = auth_setting.create_token(user_data,15)

    
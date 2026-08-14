from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from workhub.auth.models import User
from workhub.auth.setting import auth_setting
from workhub.auth.setting.notify_setting import send_reset_link
from workhub.db_connection import get_db
from ..schemas import CreateUser

router = APIRouter(tags=["User Authentication"])


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
        if get_user_data.is_active:
            return get_user_data
        else:
            raise HTTPException(detail="User is deactivated", status_code=403)

    # if user not exist then we will have a error

    raise HTTPException(detail="Username not found", status_code=404)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Login endpoint.

    - Get user from DB using username
    - Verify password with stored hash
    - If valid, create JWT token (OAuth2)
    - Return token for authentication

    Args:
        form_data: username and password from request
        db: database session

    Returns:
        JWT token string
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
def forgot_password(username: str, db: Session = Depends(get_db)):
    """
    Forgot password endpoint.

    - Check if user exists in DB using username
    - Create a short-lived token (15 min)
    - Build reset link with that token
    - Send reset link to user's email

    Args:
        username: user account name
        db: database session

    Returns:
        None (sends email with reset link)
    """

    get_user_data = get_user(username, db)
    user_data = {"sub": get_user_data.username}
    token = auth_setting.create_token(user_data, 15)
    return send_reset_link(
        get_user_data.email_id, f"http://127.0.0.1:8000/reset_password?{token}"
    )


@router.post("/reset_password")
def user_reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    """
    Reset password endpoint.

    - Verify token and get username
    - Find user in DB
    - Hash the new password
    - Update user record and commit changes

    Args:
        token: JWT token from reset link
        new_password: new password string
        db: database session

    Returns:
        dict with success message
    """
    username = auth_setting.verify_token(token)

    user_data = db.query(User).filter(User.username == username).first()
    hashed_password = auth_setting.password_hash(new_password)
    user_data.password = hashed_password
    db.commit()
    db.refresh(user_data)
    return {"msg": "Password reset successful"}

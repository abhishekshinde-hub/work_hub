from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from workhub.auth import service
from workhub.db_connection import get_db
from .schemas import CreateUser

router = APIRouter(tags=["User Authentication"])


@router.post("/register")
def user_register(request: CreateUser, db: Session = Depends(get_db)):
    return service.register_user(request, db)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    return service.user_login(form_data, db)


@router.post("/forgot_password/{username}")
def forgot_password(username: str, db: Session = Depends(get_db)):
    return service.serivce_forgot_password(username, db)


@router.post("/reset_password")
def user_reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    return service.service_reset_password(token, new_password, db)


@router.post("/logout")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    return service.service_refresh_token(refresh_token, db)


@router.post("/get_access_token")
def get_new_access_token(refresh_token: str, db: Session = Depends(get_db)):
    return service.get_new_access_token(refresh_token,db)

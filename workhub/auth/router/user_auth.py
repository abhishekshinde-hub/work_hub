from argon2 import PasswordHasher
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from workhub.auth.models import User
from workhub.auth.router import auth_setting
from ..schemas import CreateUser, LoginUser
from db_connection import get_db
import jwt

router = APIRouter()



"""This funtion that help users to make there new account (register user) in workhub"""
@router.post('/register')
def user_register(request : CreateUser, db : Session = Depends(get_db)) : 
    print("this is the password ",request.password)
    hashed_password = auth_setting.password_hash(request.password)
    user_data = User(name = request.name, gender = request.gender, role = request.role, username = request.username, password = hashed_password, email_id = request.email_id, mobile_no = request.mobile_no)
    try : 
        db.add(user_data)
        db.commit()
        db.refresh(user_data)
        return {"message" : "user registration successfull"}
    except Exception as e:
        print("=====================")
        print("thsi is the erroor",e)
        raise HTTPException( detail=f"Error: {str(e)}", status_code = 400)

def get_user(username,db) : 
    try:
        return db.query(User).filter(User.username == username).first()
        
    except:
        raise HTTPException(detail="Username not found", status = 404)

@router.post('/login')
def login(request : LoginUser, db : Session = Depends(get_db)):
    user_data =  get_user(request.username, db)
    auth_setting.verify_password(user_data.password, request.password)
    user_data = {"username": user_data.username, "email": user_data.email_id}
    token = auth_setting.create_token(user_data)
    print("this is the user data", user_data)
    return {"access" : token}
    
    



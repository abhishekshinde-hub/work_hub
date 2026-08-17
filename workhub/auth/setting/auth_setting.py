from datetime import datetime, timedelta, timezone
import jwt
from argon2 import PasswordHasher
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from workhub.auth.models import User
from workhub.db_connection import get_db

SECRET_KEY = "i am abhishek shinde from indore"

Oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login")


"""PasswordHasher it is a module that we get pwdlib-argon2 it help us to hash the password so that no one can hack password"""

hash_password = PasswordHasher()


def password_hash(password):
    """
    we call it at user register time
    This funtion help us to hash the password it means convert noraml password in encrypted form
    """
    return hash_password.hash(password)


def verify_password(hashed_password, plan_password):
    """
    This funtion check to user password weather is correct not decrypt user encrypted password
    """
    try:
        hash_password.verify(hashed_password, plan_password)
    except:
        raise HTTPException(detail="password not matched", status_code=401)

#==================================================================================================

def create_token(data: dict, expire_time: timedelta | None = None):
    """
    This funtion we call when login api run , it passes useinfo  in data args Like (username,user_id)
    when it check user data and security key and alogorithm , and help us to create token .

    """
    jwt_payload = data.copy()

    if expire_time:
        token_expire_time = datetime.now(timezone.utc) +  timedelta(minutes=expire_time)
    else:
        token_expire_time = datetime.now(timezone.utc) + timedelta(minutes=15)
    try:
        jwt_payload.update({"exp": token_expire_time})
        return jwt.encode(jwt_payload, SECRET_KEY, algorithm="HS256")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Token generation failed: {str(e)}"
        )


def verify_token(token: str = Depends(Oauth_scheme)):
    print("bhia token aaya",token)
    """
    It runs when user try to login at this time it decrypt user access token like expire time and other details
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        role = payload.get("role")

        print("this user name =", username)
        if not username:
            raise HTTPException(
                detail="Invalid token", status_code=status.HTTP_401_UNAUTHORIZED
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError as e:
        print("Toked decoded time error =>", e)
        raise HTTPException(status_code=401, detail="Could not validate token")
    return {"username" : username, "role" : role}


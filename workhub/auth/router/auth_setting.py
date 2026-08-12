from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from fastapi import HTTPException

SECRET_KEY = "i am abhishek shinde from indore"
def create_token(data : dict, expire_time : timedelta | None = None) :
    jwt_payload = data.copy()
    
    if expire_time :
        token_expire_time = datetime.now(timezone.utc)+timedelta(minutes=expire_time)
    else : 
        token_expire_time = datetime.now(timezone.utc)+timedelta(minutes=15)
    try : 
        jwt_payload.update({"exp" : token_expire_time})
        return jwt.encode(jwt_payload,SECRET_KEY,algorithm = "HS256")
    except Exception as e :
        raise HTTPException( status_code=500,
        detail=f"Token generation failed: {str(e)}")


"""PasswordHasher it is a module that we get pwdlib-argon2 it help us to hash the password so that no one can hack password"""

hash_password = PasswordHasher()

def password_hash(password) : 
    print("now i am in the password of setting of auth",password)
    return hash_password.hash(password)


def verify_password(hashed_password, plan_password) : 
    try : 
        hash_password.verify(hashed_password, plan_password)
    except : 
        raise HTTPException(detail = "password not matched",status_code = 401)
    
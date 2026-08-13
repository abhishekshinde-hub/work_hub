from fastapi import APIRouter, Depends, HTTPException, status
from workhub.auth.models import User
from workhub.auth.setting.auth_setting import verify_token
from workhub.db_connection import get_db
from workhub.user_profile.schema import UpdateUserDetail
from sqlalchemy.orm import Session


router = APIRouter(tags= ["user profile"])
database = Depends(get_db)

@router.put("/user", status_code = 200)
def update_user_detail(request : UpdateUserDetail,user_data : User = Depends(verify_token) ) :
    print(user_data)
   
    
    
    
    
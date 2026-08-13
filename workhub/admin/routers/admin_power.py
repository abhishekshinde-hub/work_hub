from fastapi import Depends,status, HTTPException, APIRouter
from workhub.auth.models import User
from workhub.db_connection import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags= ["admin"])

@router.get('/users',status_code= 200)
def get_all_users(db : Session = Depends(get_db)):
    user_data  = db.query(User).all()
    if user_data :
        return user_data
    raise HTTPException (detail =  "user not exist", status_code = 404)


def get_user(id, db) : 

    data = db.query(User).filter(User.user_id == id).first()
    if data : 
        return data
    else : 
        raise HTTPException(detail = "User not found", status_code = status.HTTP_404_NOT_FOUND)

    
@router.get("/users/{id}", status_code = 200)
def get_single_user(id : int,db : Session = Depends(get_db)) : 
    user_data = get_user(id, db)
    return user_data
@router.delete("/users/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_user(id :int,db :Session = Depends(get_db)) : 
    user_data = get_user(id,db)
    db.delete(user_data)
    db.commit()
    
    return {"message" : "account was deleted"}

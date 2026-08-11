from pydantic import BaseModel
from enum import Enum

class Role(str,Enum) : 
    admin = "admin"
    manager = "manager"
    developer = "developer"
class Gender(str,Enum) : 
    male = "Male"
    Female = "Female"
class CreateUser(BaseModel) :
    name : str
    email : str
    username :str
    password :str
    gender : Gender
    role : Role.developer

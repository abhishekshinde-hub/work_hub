from pydantic import BaseModel
class UpdateUserDetail(BaseModel) : 
    name : str
    email_id : str
    mobile_no :str
    gender : str
    

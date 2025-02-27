from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

# USER
class CreateUser(BaseModel):
    email: str
    password: str = Field(..., min_length=4) # For 1 big letter, 1 small letter, 1 number, 1 special character and min 8 characters: pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

class GetUser(BaseModel):
    id: int
    email: str
    updated_at: datetime
    created_at: datetime        
    
class LoginUser(BaseModel):
    email: str
    password: str
    
# Token
class Token(BaseModel):
    user_id: int
    exp: datetime


# POST
class GetPost(BaseModel):
    id: int
    text: str
    user_id: int
    updated_at: datetime
    created_at: datetime
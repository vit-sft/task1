from datetime import datetime

import jwt
import os

from models import dto

  
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "e5f9d1ccfb8321213154241f326638887579-4a2bd123213bb71ef1e83ec53c80559299_311s")
ALGORITHM = "HS256"

def encode(user_id: int, exp: datetime) -> str:
    token = dto.Token(
        user_id=user_id,
        exp=exp,
    )
    return jwt.encode(token.model_dump(), SECRET_KEY, algorithm=ALGORITHM)
    
def decode(token: str) -> dto.Token | None:
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return dto.Token(**token_data)
    except jwt.PyJWTError as e:
        # print(e)
        return None
    
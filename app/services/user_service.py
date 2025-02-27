from random import randint

from models import db
from repos import user_repo

from utils.bcrypt_hashing import HashLib
from utils import formating
            
def get_by_id(id: int) -> db.User | None:
    return user_repo.get_by_id(id)
    
def get_by_email(email: str) -> db.User | None:
    return user_repo.get_by_email(email.lower().strip())

def create(email: str, password: str) -> db.User:
    email = formating.format_string(email)
    pass_hash = HashLib.hash(password)
    return user_repo.add(email, pass_hash)
    
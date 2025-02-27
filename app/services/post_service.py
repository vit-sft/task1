from models import db
from repos import post_repo
from fastapi import HTTPException

from cachetools import TTLCache
from functools import lru_cache

posts_cache = TTLCache(maxsize=1000, ttl=300)

def add(text: str, user_id: int) -> db.Post:
    # Validate payload size (1 MB = 1,048,576 bytes)
    if text and len(text.encode('utf-8')) > 1048576:
        raise HTTPException(status_code=413, detail="Payload too large")
    
    return post_repo.add(text, user_id)

def get_posts(user_id: int) -> list[db.Post]:
    if user_id in posts_cache:
        return posts_cache[user_id]
    
    posts = post_repo.get_posts(user_id)
    posts_cache[user_id] = posts
    return posts

def delete_post(id: int, user_id: int) -> int:
    return post_repo.delete_post(id, user_id)
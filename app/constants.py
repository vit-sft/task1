from datetime import timedelta
from os import getenv


DB_CONNECTION_STRING = getenv("DB_CONNECTION_STRING")
COOKIES_KEY_NAME = "session_token"
SESSION_TIME = timedelta(days=30)
HASH_SALT = getenv("HASH_SALT", "e5f9d1ccfb848554f5850954241f326638887579-4a2bd61027057378fbb71ef1e83ec53c80559299_123s")
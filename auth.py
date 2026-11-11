"""Password hashing and login tokens for user accounts."""
import os
import secrets
from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

# The key that signs login tokens. Set SECRET_KEY so tokens keep working
# after the server restarts. Without it a random key is made at start-up.
SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Checked when the username does not exist, so a wrong username takes as
# long as a wrong password and cannot be guessed from the response time.
DUMMY_HASH = password_hash.hash("not-a-real-password")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(username: str) -> str:
    expires = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": username, "exp": expires}, SECRET_KEY, algorithm=ALGORITHM)

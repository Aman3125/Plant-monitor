"""Password hashing for user accounts.

Passwords are never saved as plain text. They are hashed with Argon2,
and a login is checked by comparing the typed password to the hash.
"""
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

import time
import jwt
from passlib.context import CryptContext

SECRET_KEY = "CHANGE_THIS_TO_A_LONG_RANDOM_SECRET"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["pbkdf2_sha256"],default="pbkdf2_sha256",deprecated="auto")

# Example user database (replace with real DB later)
users_db = {
    "maurice": pwd_context.hash("password123"),
    "coworker1": pwd_context.hash("mypassword"),
}

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def authenticate_user(username, password):
    if username not in users_db:
        return False
    if not verify_password(password, users_db[username]):
        return False
    return True

def create_token(username):
    payload = {
        "sub": username,
        "exp": time.time() + 3600  # 1 hour expiry
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded["sub"]
    except:
        return None

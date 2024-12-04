from models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashPassword(password: str) -> str:
    return pwd_context.hash(password)

def verifyPassword(encoded_password: str, decoded_password: str) -> bool:
    return pwd_context.verify(decoded_password, encoded_password)

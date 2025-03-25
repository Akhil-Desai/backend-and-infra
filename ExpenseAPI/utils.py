import bcrypt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from datetime import datetime
import jwt


#*Password Authentication
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


#-----------------------------
#* Authenticate JWT Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/v1/login")
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        #JWT library (jwt.decode) validates "exp" already no need to implement
        user_id = payload.get("sub")
    except jwt.PyJWTError as e:
        raise HTTPException(401, detail=str(e))

    return user_id

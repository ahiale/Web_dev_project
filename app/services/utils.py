from passlib.hash import pbkdf2_sha256  # type: ignore
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.schemas.userSchema import DataToken
from database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = "MTvlleCfHF1kBweAyyRRO3ufTajxeHvrqWyrcfmDx3r7HpvXbSG3JgRQUoCZLySz" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_hashed_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return pbkdf2_sha256.verify(password, hashed_pass)

def create_access_token(user_id: int):
    to_encode = {"user_id": user_id}

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_token_access(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception

        token_data = DataToken(id=user_id)
        
    except JWTError as e:
        print(e)
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token_access(token, credentials_exception)
    user = db.query(User).filter(User.id == token_data.id).first()
    if not user:
        raise credentials_exception

    return user

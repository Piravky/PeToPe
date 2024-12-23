from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends, status, HTTPException
from jose.exceptions import JWTError
from sqlalchemy.orm import Session
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from dependencies import get_session
from config import settings
from models import User

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token")



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy( )
  if expires_delta:
    expire = datetime.now() + expires_delta
  else:
    expire = datetime.now() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
  return encoded_jwt

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_session)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
  )
  try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    email: str = payload.get("sub")
    if email is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception

  user = db.query(User).filter(User.email == email).first() #FIXME: заменить на методы для базы данных

  if not user:
    raise credentials_exception
  return user

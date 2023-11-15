from passlib.context import CryptContext
import hashlib
import hmac
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

from bin.settings.settings import settings


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def generate_secret_key(key: str) -> str:
    payload = settings.JWT_SECRET_KEY
    secret_key = hmac.new(key.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return secret_key

def generate_oauth_access_token_id(key: str) -> str:
    payload = "@!WE$%#@@@@@@@@DS@"
    secret_key = hmac.new(key.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return secret_key


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def validate_key(db, x_client_id: str, x_secret_id: str) -> bool:
    if x_client_id is None or x_secret_id is None:
        return False
        
    keys = db.execute("SELECT oc.secret as x_client_secret, oat.id as x_client_id FROM oauth_clients as oc \
        LEFT JOIN oauth_access_tokens as oat ON oc.user_id = oat.user_id WHERE oc.secret = :x_client_secret AND oat.id = :x_client_id",\
            {"x_client_id":x_client_id, "x_client_secret": x_secret_id}).fetchone()
    if not keys:
        return False
    else:
        return True


def manipulated_string(param):
    if param == None:    
        return param

    data = param.split('status_', 1)
    return data[1].replace("_", " ")
    

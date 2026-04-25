from jose import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.config import settings


JWT_SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.ALGORITHM

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        affiliate_id = payload.get("id")
        if affiliate_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return affiliate_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
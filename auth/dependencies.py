from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from database import get_db
from models import user as models_user
from .security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models_user.User).filter(models_user.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_superadmin(current_user: models_user.User = Depends(get_current_user)):
    if current_user.role != models_user.UserRole.superadmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hak akses ditolak. Hanya Super Admin yang diizinkan."
        )
    return current_user

def get_current_admin(current_user: models_user.User = Depends(get_current_user)):
    # Memeriksa apakah user adalah admin atau superadmin
    if current_user.role not in [models_user.UserRole.superadmin, models_user.UserRole.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hak akses ditolak. Hanya Super Admin dan Admin yang diizinkan."
        )
    return current_user
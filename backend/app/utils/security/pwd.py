import bcrypt
from sqlalchemy.orm import Session

from app.database import User
from app.utils.check_db import get_user_or_404

def hash_pwd(pwd: str) -> str:
    """Hashes the given password with salt.
    """
    
    salt = bcrypt.gensalt()
    bytes = pwd.encode('utf-8')
    hash = bcrypt.hashpw(bytes, salt)
    
    return hash.decode("utf-8") 

def verify_pwd(given_pwd: str, hash: str) -> bool:
    """Checks if the given password is correct.
    """
    
    return bcrypt.checkpw(given_pwd.encode("utf-8"), hash.encode("utf-8"))

def authenticate_user(username: str, pwd: str, session: Session) -> User | None:
    user = get_user_or_404(username, session)
    if not user or not verify_pwd(pwd, user.hashed_password):
        return
    return user
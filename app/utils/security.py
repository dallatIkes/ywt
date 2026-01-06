import bcrypt

def hash_pwd(pwd: str) -> str:
    """Hashes the given password with salt.
    """
    
    salt = bcrypt.gensalt()
    bytes = pwd.encode('utf-8')
    hash = bcrypt.hashpw(bytes, salt)
    
    return hash
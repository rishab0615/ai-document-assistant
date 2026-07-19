from passlib.context import CryptContext

pwd_context = CryptContext(                  # This is used to perform hashing operations
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):            
    return pwd_context.hash(password)           # Return hashed


def verify_password(plain_password: str, hashed_password: str):    
    return pwd_context.verify(plain_password,hashed_password)                 # Return true or false
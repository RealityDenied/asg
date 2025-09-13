from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import hashlib
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models import TokenData, User, UserInDB, UserCreate

# JWT config
SECRET_KEY = "my-secret-key-change-in-production-123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# simple password hashing
def verify_password(plain_password, hashed_password):
    """check if password  matches"""
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def get_password_hash(password):
    """hash the password"""
    return hashlib.sha256(password.encode()).hexdigest()

# bearer token setup
security = HTTPBearer(auto_error=True)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """create jwt  token"""
    to_encode = data.copy()
    if expires_delta:
        expire  = datetime.utcnow()+ expires_delta
    else:
        expire= datetime.utcnow()+ timedelta(minutes=15)
    to_encode.update({"exp": expire})
    token=  jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return  token

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """verify jwt token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token_data: TokenData = Depends(verify_token)):
    """get user from token"""
    # return mock user for demo
    user = User(username=token_data.username, full_name="Demo User")
    return user

# user database - should be in mongo in real app
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": get_password_hash("admin123"),
        "email": "admin@company.com",
        "full_name": "System Administrator",
        "disabled": False,
    },
    "user": {
        "username": "user", 
        "hashed_password": get_password_hash("user123"),
        "email": "user@company.com",
        "full_name": "Regular User",
        "disabled": False,
    }
}

def authenticate_user(username: str, password: str):
    """check user login"""
    # check fake users first
    user = fake_users_db.get(username)
    if user and verify_password(password, user["hashed_password"]):
        return UserInDB(**user)
    
    # check mongo db
    from app.configurations import users_collection
    db_user = users_collection.find_one({"username": username})
    if db_user and verify_password(password, db_user["hashed_password"]):
        db_user["_id"] = str(db_user["_id"])
        return UserInDB(**db_user)
    
    return False

def create_user(user_data: UserCreate):
    """create new user"""
    from app.configurations import users_collection
    
    # check if username exists
    if user_data.username in fake_users_db:
        return None
    
    # check mongo too
    existing_user = users_collection.find_one({"username": user_data.username})
    if existing_user:
        return None
    
    # create user
    hashed_password = get_password_hash(user_data.password)
    new_user = {
        "username": user_data.username,
        "hashed_password": hashed_password,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "disabled": False,
        "created_at": datetime.utcnow()
    }
    
    # save to db
    result = users_collection.insert_one(new_user)
    
    # add to fake db for quick access
    fake_users_db[user_data.username] = new_user
    
    return UserInDB(**new_user)

def get_user_from_db(username: str):
    """get user from db"""
    from app.configurations import users_collection
    
    # check fake db first
    if username in fake_users_db:
        return UserInDB(**fake_users_db[username])
    
    # check mongo
    user = users_collection.find_one({"username": username})
    if user:
        user["_id"] = str(user["_id"])
        return UserInDB(**user)
    
    return None
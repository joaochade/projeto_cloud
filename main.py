from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from database import Base, get_db, engine
from models import User
import requests


SECRET_KEY = "9f51b569a063c9ae966e44757dfd71e853681a1bf9064444c0cd6afd87c48382"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
app = FastAPI()

Base.metadata.create_all(bind=engine)


GEEK_JOKE_API_URL = "https://geek-jokes.sameerkumar.website/api?format=json"

class Token(BaseModel):
    access_token: str
    # token_type: str

class TokenData(BaseModel):
    email: Union[str, None] = None

class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UserResponse(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def fetch_joke():
    response = requests.get(GEEK_JOKE_API_URL)
    if response.status_code != 200:
        raise HTTPException(status_code=503, detail="Failed to fetch joke")
    return response.json()

@app.post("/registrar", response_model=Token)
async def registrar(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    hashed_password = get_password_hash(user.senha)
    new_user = User(
        username=user.nome,
        email=user.email,
        hashed_password=hashed_password,
        disabled=False
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        print(f"Error saving new user: {e}")
        raise HTTPException(status_code=500, detail="Error saving new user")

    try:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": new_user.email}, expires_delta=access_token_expires)
    except Exception as e:
        print(f"Error generating token: {e}")
        raise HTTPException(status_code=500, detail="Error generating token")

    return Token(access_token=access_token)


@app.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except PyJWTError:
        raise credentials_exception

    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


@app.get("/users/me/", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[UserResponse, Depends(get_current_user)]
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[UserResponse, Depends(get_current_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]


async def get_current_active_user(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/consultar")
async def consultar(current_user: User = Depends(get_current_user)):
    try:
        joke_data = fetch_joke()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch joke")
    
    return joke_data

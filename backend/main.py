from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime, timedelta
from typing import Optional, List
import jwt
import hashlib
import os
from models import User, Mug, SwipeAction, UserCreate, UserLogin, MugResponse, Base
from database import engine, SessionLocal
from sqlalchemy.orm import Session

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mugswap API", description="A Tinder-style app for coffee mugs")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")
ALGORITHM = "HS256"


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.post("/api/auth/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_password = hash_password(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        age=user.age,
        bio=user.bio,
        password_hash=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": db_user.id, "email": db_user.email, "name": db_user.name},
    }


@app.post("/api/auth/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": db_user.id, "email": db_user.email, "name": db_user.name},
    }


@app.get("/api/mugs", response_model=List[MugResponse])
async def get_mugs(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    # Get mugs that user hasn't swiped on
    swiped_mug_ids = (
        db.query(SwipeAction.mug_id)
        .filter(SwipeAction.user_id == current_user.id)
        .all()
    )
    swiped_ids = [id[0] for id in swiped_mug_ids]

    mugs = db.query(Mug).filter(~Mug.id.in_(swiped_ids)).limit(10).all()
    return mugs


@app.post("/api/swipe")
async def swipe(
    mug_id: int,
    is_like: bool,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check if already swiped
    existing_swipe = (
        db.query(SwipeAction)
        .filter(SwipeAction.user_id == current_user.id, SwipeAction.mug_id == mug_id)
        .first()
    )

    if existing_swipe:
        raise HTTPException(status_code=400, detail="Already swiped on this mug")

    # Create swipe action
    swipe = SwipeAction(user_id=current_user.id, mug_id=mug_id, is_like=is_like)
    db.add(swipe)
    db.commit()

    return {"success": True, "is_like": is_like}


@app.get("/api/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "age": current_user.age,
        "bio": current_user.bio,
    }


@app.get("/api/matches")
async def get_matches(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    # Get mugs the user liked
    liked_mugs = (
        db.query(Mug)
        .join(SwipeAction)
        .filter(SwipeAction.user_id == current_user.id, SwipeAction.is_like.is_(True))
        .all()
    )
    return liked_mugs


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

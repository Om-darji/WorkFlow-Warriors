from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List

# Internal imports
from . import models, schemas, database  

app = FastAPI(title="Traveloop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return RedirectResponse(url="/static/landing.html")

# --- AUTHENTICATION ---

@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # 1. Check if user already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Create User
    new_user = models.User(
        email=user.email,
        full_name=user.full_name,
        password_hash=user.password  # To be hashed in production
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    # 1. Fetch user
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    # 2. Validate
    if not user or user.password_hash != user_credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )

    return {
        "message": "Login successful", 
        "user_id": user.id,
        "full_name": user.full_name
    }

@app.put("/reset-password")
def reset_password(email: str, new_password: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.password_hash = new_password
    db.commit()
    return {"message": "Password updated successfully"}

@app.post("/trips", response_model=schemas.TripResponse)
def create_trip(trip: schemas.TripCreate, user_id: int, db: Session = Depends(database.get_db)):
    # Relational Check: Verify user exists before creating trip
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    new_trip = models.Trip(**trip.dict(), user_id=user_id)
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    return new_trip

@app.get("/trips/{user_id}", response_model=List[schemas.TripResponse])
def get_my_trips(user_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Trip).filter(models.Trip.user_id == user_id).all()

# Should be at the bottom of main.py
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
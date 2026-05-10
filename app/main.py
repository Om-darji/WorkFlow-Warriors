from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import models
from app import database  

app = FastAPI(title="Traveloop API")

# Allow frontend to connect with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home Route
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Traveloop API - Backend Running Successfully"
    }


# Login Endpoint
@app.post("/login")
def login(
    email: str,
    password: str,
    db: Session = Depends(database.get_db)
):

    # Find user by email
    user = db.query(models.User).filter(
        models.User.email == email
    ).first()

    # User not found
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Password check
    if user.password_hash != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    # Success response
    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }
    }
from fastapi import UploadFile, File, Form
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


    # Dashboard Endpoint
    @app.get("/dashboard")
    def get_dashboard():
        dashboard_data = {
            "welcome_message": "Welcome Back, Traveler ✈️",
            "stats": {
                "total_trips": 12,
                "countries_visited": 8,
                "total_budget": 120000,
                "upcoming_trips": 3
            },
            "recent_trips": [
                {
                    "destination": "Paris",
                    "days": 5,
                    "budget": 45000
                },
                {
                    "destination": "Tokyo",
                    "days": 7,
                    "budget": 82000
                },
                {
                    "destination": "Dubai",
                    "days": 4,
                    "budget": 60000
                }
            ],
            "recommended_destinations": [
                "Goa",
                "Switzerland",
                "Bali"
            ]
        }
        return dashboard_data


    # Create Trip Endpoint
    @app.post("/trips/create")
    async def create_trip(
        trip_name: str = Form(...),
        start_date: str = Form(...),
        end_date: str = Form(...),
        description: str = Form(...),
        cover_photo: UploadFile = File(None)
    ):
        # Here you would typically save the trip to the database and handle the file upload
        # For now, just return the received data
        trip_data = {
            "trip_name": trip_name,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
            "cover_photo_filename": cover_photo.filename if cover_photo else None
        }
        return {"message": "Trip created successfully", "trip": trip_data}
# Trip Notes / Journal Endpoints
from datetime import datetime

# Example in-memory notes store (replace with DB in production)
trip_notes = {}

# Get notes for a trip (optionally per stop)
@app.get("/trips/{trip_id}/notes")
def get_trip_notes(trip_id: int, stop: str = None):
    notes = trip_notes.get(trip_id, [])
    if stop:
        notes = [n for n in notes if n.get("stop") == stop]
    # Sort by timestamp descending
    notes = sorted(notes, key=lambda n: n["timestamp"], reverse=True)
    return {"notes": notes}

# Add note
@app.post("/trips/{trip_id}/notes/add")
def add_trip_note(trip_id: int, text: str, stop: str = None):
    notes = trip_notes.setdefault(trip_id, [])
    note_id = max([n["id"] for n in notes], default=0) + 1
    note = {
        "id": note_id,
        "text": text,
        "stop": stop,
        "timestamp": datetime.utcnow().isoformat()
    }
    notes.append(note)
    return {"message": "Note added", "note": note}

# Edit note
@app.post("/trips/{trip_id}/notes/edit")
def edit_trip_note(trip_id: int, note_id: int, text: str):
    notes = trip_notes.setdefault(trip_id, [])
    for n in notes:
        if n["id"] == note_id:
            n["text"] = text
            n["timestamp"] = datetime.utcnow().isoformat()
            return {"message": "Note updated", "note": n}
    return {"error": "Note not found"}

# Delete note
@app.delete("/trips/{trip_id}/notes/delete")
def delete_trip_note(trip_id: int, note_id: int):
    notes = trip_notes.setdefault(trip_id, [])
    for n in notes:
        if n["id"] == note_id:
            notes.remove(n)
            return {"message": "Note deleted", "note_id": note_id}
    return {"error": "Note not found"}
# User Profile / Settings Endpoints
from fastapi import HTTPException

# Example in-memory user store (replace with DB in production)
user_profiles = {
    1: {
        "id": 1,
        "name": "Traveler123",
        "email": "traveler@example.com",
        "photo_url": "https://example.com/photo.jpg",
        "language": "en",
        "saved_destinations": ["Paris", "Tokyo", "Goa"]
    }
}

# Get user profile
@app.get("/user/profile/{user_id}")
def get_user_profile(user_id: int):
    user = user_profiles.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user profile
@app.post("/user/profile/{user_id}/update")
def update_user_profile(user_id: int, name: str = None, email: str = None, photo_url: str = None):
    user = user_profiles.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if name:
        user["name"] = name
    if email:
        user["email"] = email
    if photo_url:
        user["photo_url"] = photo_url
    return {"message": "Profile updated", "user": user}

# Set language preference
@app.post("/user/profile/{user_id}/language")
def set_language(user_id: int, language: str):
    user = user_profiles.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["language"] = language
    return {"message": "Language updated", "language": language}

# Delete account
@app.delete("/user/profile/{user_id}/delete")
def delete_account(user_id: int):
    if user_id in user_profiles:
        del user_profiles[user_id]
        return {"message": "Account deleted"}
    raise HTTPException(status_code=404, detail="User not found")

# Get saved destinations
@app.get("/user/profile/{user_id}/saved-destinations")
def get_saved_destinations(user_id: int):
    user = user_profiles.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"saved_destinations": user.get("saved_destinations", [])}
# Shared/Public Itinerary View Endpoint
@app.get("/public/itinerary/{public_id}")
def public_itinerary_view(public_id: str):
    # Example static public itinerary data; replace with DB query in production
    itinerary = {
        "public_id": public_id,
        "trip_name": "Europe Adventure",
        "summary": "A 2-week journey through Paris and Rome, packed with culture, food, and adventure.",
        "owner": "Traveler123",
        "days": [
            {
                "city": "Paris",
                "date": "2026-06-01",
                "activities": [
                    {"name": "Eiffel Tower", "time": "10:00", "cost": 25},
                    {"name": "Louvre Museum", "time": "14:00", "cost": 20}
                ]
            },
            {
                "city": "Rome",
                "date": "2026-06-06",
                "activities": [
                    {"name": "Colosseum", "time": "09:00", "cost": 18},
                    {"name": "Vatican City", "time": "13:00", "cost": 22}
                ]
            }
        ],
        "share_url": f"https://traveloop.com/public/itinerary/{public_id}",
        "can_copy": True,
        "read_only": True
    }
    return itinerary
# Packing Checklist Endpoints
from fastapi import Query

# Example in-memory checklist store (replace with DB in production)
packing_checklists = {}

# Get checklist
@app.get("/trips/{trip_id}/packing-checklist")
def get_packing_checklist(trip_id: int):
    checklist = packing_checklists.get(trip_id, [
        {"id": 1, "item": "Passport", "packed": False, "category": "documents"},
        {"id": 2, "item": "T-Shirts", "packed": False, "category": "clothing"},
        {"id": 3, "item": "Phone Charger", "packed": False, "category": "electronics"}
    ])
    return {"checklist": checklist}

# Add item
@app.post("/trips/{trip_id}/packing-checklist/add")
def add_packing_item(trip_id: int, item: str = Query(...), category: str = Query("other")):
    checklist = packing_checklists.setdefault(trip_id, [])
    new_id = max([i["id"] for i in checklist], default=0) + 1
    new_item = {"id": new_id, "item": item, "packed": False, "category": category}
    checklist.append(new_item)
    return {"message": "Item added", "item": new_item}

# Update (mark packed/unpacked)
@app.post("/trips/{trip_id}/packing-checklist/mark")
def mark_packing_item(trip_id: int, item_id: int = Query(...), packed: bool = Query(...)):
    checklist = packing_checklists.setdefault(trip_id, [])
    for i in checklist:
        if i["id"] == item_id:
            i["packed"] = packed
            return {"message": "Item updated", "item": i}
    return {"error": "Item not found"}

# Remove item
@app.delete("/trips/{trip_id}/packing-checklist/remove")
def remove_packing_item(trip_id: int, item_id: int = Query(...)):
    checklist = packing_checklists.setdefault(trip_id, [])
    for i in checklist:
        if i["id"] == item_id:
            checklist.remove(i)
            return {"message": "Item removed", "item_id": item_id}
    return {"error": "Item not found"}

# Reset checklist
@app.post("/trips/{trip_id}/packing-checklist/reset")
def reset_packing_checklist(trip_id: int):
    packing_checklists[trip_id] = []
    return {"message": "Checklist reset"}
# Trip Budget & Cost Breakdown Endpoint
@app.get("/trips/{trip_id}/budget")
def trip_budget_breakdown(trip_id: int):
    # Example static budget data; replace with DB query in production
    budget = {
        "total_estimated_cost": 3500,
        "breakdown": {
            "transport": 900,
            "stay": 1200,
            "activities": 800,
            "meals": 600
        },
        "average_cost_per_day": 350,
        "over_budget_days": [
            {"date": "2026-06-03", "amount": 420},
            {"date": "2026-06-07", "amount": 410}
        ],
        "chart_data": {
            "labels": ["Transport", "Stay", "Activities", "Meals"],
            "values": [900, 1200, 800, 600]
        }
    }
    return budget
# Activity Search Endpoint
@app.get("/activities/search")
def search_activities(
    query: str = "",
    activity_type: str = None,
    min_cost: int = 0,
    max_cost: int = 1000,
    min_duration: int = 0,
    max_duration: int = 24
):
    # Example static activity data; replace with DB query in production
    all_activities = [
        {
            "name": "Eiffel Tower Tour",
            "type": "Sightseeing",
            "cost": 25,
            "duration": 2,
            "description": "Visit the iconic Eiffel Tower.",
            "image_url": "https://example.com/eiffel.jpg"
        },
        {
            "name": "Louvre Museum",
            "type": "Culture",
            "cost": 20,
            "duration": 3,
            "description": "Explore world-famous art collections.",
            "image_url": "https://example.com/louvre.jpg"
        },
        {
            "name": "Seine River Cruise",
            "type": "Sightseeing",
            "cost": 30,
            "duration": 1,
            "description": "Cruise along the Seine River.",
            "image_url": "https://example.com/seine.jpg"
        },
        {
            "name": "Food Tour Rome",
            "type": "Food",
            "cost": 40,
            "duration": 4,
            "description": "Taste authentic Roman cuisine.",
            "image_url": "https://example.com/foodtour.jpg"
        },
        {
            "name": "Vatican City Visit",
            "type": "Culture",
            "cost": 22,
            "duration": 3,
            "description": "Discover the Vatican's treasures.",
            "image_url": "https://example.com/vatican.jpg"
        },
        {
            "name": "Surfing Bali",
            "type": "Adventure",
            "cost": 50,
            "duration": 5,
            "description": "Catch waves on Bali's beaches.",
            "image_url": "https://example.com/surfing.jpg"
        }
    ]
    filtered = [
        a for a in all_activities
        if (query.lower() in a["name"].lower())
        and (activity_type is None or a["type"].lower() == activity_type.lower())
        and (min_cost <= a["cost"] <= max_cost)
        and (min_duration <= a["duration"] <= max_duration)
    ]
    return {"results": filtered}
# City Search Endpoint
@app.get("/cities/search")
def search_cities(query: str = "", country: str = None, region: str = None):
    # Example static city data; replace with DB query in production
    all_cities = [
        {"name": "Paris", "country": "France", "cost_index": 85, "popularity": 95},
        {"name": "Rome", "country": "Italy", "cost_index": 70, "popularity": 90},
        {"name": "Tokyo", "country": "Japan", "cost_index": 95, "popularity": 98},
        {"name": "Goa", "country": "India", "cost_index": 40, "popularity": 80},
        {"name": "Bali", "country": "Indonesia", "cost_index": 50, "popularity": 88},
        {"name": "Zurich", "country": "Switzerland", "cost_index": 100, "popularity": 85}
    ]
    filtered = [
        city for city in all_cities
        if (query.lower() in city["name"].lower())
        and (country is None or city["country"].lower() == country.lower())
        and (region is None or region.lower() in city["country"].lower())
    ]
    return {"results": filtered}
# Itinerary View Endpoint
@app.get("/trips/{trip_id}/itinerary/view")
def view_itinerary(trip_id: int, view_mode: str = "list"):
    # Example static itinerary data; replace with DB query in production
    itinerary = [
        {
            "city": "Paris",
            "days": [
                {
                    "date": "2026-06-01",
                    "activities": [
                        {"name": "Eiffel Tower", "time": "10:00", "cost": 25},
                        {"name": "Seine River Cruise", "time": "15:00", "cost": 30}
                    ]
                },
                {
                    "date": "2026-06-02",
                    "activities": [
                        {"name": "Louvre Museum", "time": "11:00", "cost": 20}
                    ]
                }
            ]
        },
        {
            "city": "Rome",
            "days": [
                {
                    "date": "2026-06-06",
                    "activities": [
                        {"name": "Colosseum", "time": "09:00", "cost": 18},
                        {"name": "Vatican City", "time": "13:00", "cost": 22}
                    ]
                }
            ]
        }
    ]
    return {
        "trip_id": trip_id,
        "view_mode": view_mode,
        "itinerary": itinerary
    }
from fastapi import Body
# Itinerary Builder Endpoint
@app.post("/trips/{trip_id}/itinerary")
def build_itinerary(
    trip_id: int,
    stops: list = Body(..., example=[
        {
            "city": "Paris",
            "start_date": "2026-06-01",
            "end_date": "2026-06-05",
            "activities": ["Eiffel Tower", "Louvre Museum"]
        },
        {
            "city": "Rome",
            "start_date": "2026-06-06",
            "end_date": "2026-06-09",
            "activities": ["Colosseum", "Vatican City"]
        }
    ])
):
    # Here you would save the itinerary to the database
    # For now, just return the received data
    return {
        "message": "Itinerary saved successfully",
        "trip_id": trip_id,
        "itinerary": stops
    }
from typing import List
# My Trips (Trip List) Endpoint
@app.get("/trips")
def list_trips():
    # Example static data; replace with DB query in production
    trips = [
        {
            "id": 1,
            "name": "Europe Adventure",
            "start_date": "2026-06-01",
            "end_date": "2026-06-15",
            "destination_count": 4,
            "actions": ["view", "edit", "delete"]
        },
        {
            "id": 2,
            "name": "Asian Expedition",
            "start_date": "2026-08-10",
            "end_date": "2026-08-25",
            "destination_count": 3,
            "actions": ["view", "edit", "delete"]
        },
        {
            "id": 3,
            "name": "Beach Getaway",
            "start_date": "2026-12-20",
            "end_date": "2026-12-27",
            "destination_count": 2,
            "actions": ["view", "edit", "delete"]
        }
    ]
    return {"trips": trips}
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
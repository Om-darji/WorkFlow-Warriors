from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    # Links to Screen 12 (Settings/Profile)
    language_pref = Column(String(20), default="English")
    profile_pic = Column(String(255), nullable=True)

    # Relationships
    trips = relationship("Trip", back_populates="owner", cascade="all, delete-orphan")

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date)
    end_date = Column(Date)
    # Screen 9 (Budget Breakdown)
    total_budget = Column(Float, default=0.0)
    # Screen 11 (Sharing)
    is_public = Column(Boolean, default=False)
    
    # Relationships
    owner = relationship("User", back_populates="trips")
    stops = relationship("Stop", back_populates="trip", cascade="all, delete-orphan")
    packing_items = relationship("PackingItem", back_populates="trip", cascade="all, delete-orphan")
    notes = relationship("TripNote", back_populates="trip", cascade="all, delete-orphan")

class Stop(Base):
    __tablename__ = "stops"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    city_name = Column(String(100), nullable=False)
    arrival_date = Column(Date)
    departure_date = Column(Date)
    # Screen 5 (Reordering stops)
    order_index = Column(Integer, default=0)

    # Relationships
    trip = relationship("Trip", back_populates="stops")
    activities = relationship("Activity", back_populates="stop", cascade="all, delete-orphan")

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    stop_id = Column(Integer, ForeignKey("stops.id"))
    name = Column(String(100), nullable=False)
    category = Column(String(50)) # e.g., Food, Sightseeing, Transport
    cost = Column(Float, default=0.0) # For Budget Breakdown
    time_slot = Column(String(50), nullable=True) # e.g., "10:00 AM"

    stop = relationship("Stop", back_populates="activities")

class PackingItem(Base):
    __tablename__ = "packing_items"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    item_name = Column(String(100), nullable=False)
    category = Column(String(50)) # Clothing, Electronics, etc.
    is_packed = Column(Boolean, default=False)

    trip = relationship("Trip", back_populates="packing_items")

class TripNote(Base):
    __tablename__ = "trip_notes"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    trip = relationship("Trip", back_populates="notes")
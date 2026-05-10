from database import engine, Base
from models import User, Trip, Stop, Activity, PackingItem, TripNote

print("Connecting to Railway and creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully! Your cloud schema is live.")
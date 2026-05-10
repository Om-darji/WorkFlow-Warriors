import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.database import engine, Base
from app.models import User, Trip, Stop, Activity, PackingItem, TripNote

print("Connecting to Railway and creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully! Your cloud schema is live.")
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Get the URL from Railway. 
# During the hackathon, you can hardcode this for speed, 
# but in a real 'Must Have' scenario, we'd use environment variables.
# REPLACEME: Paste your Railway MYSQL_URL here
RAW_URL = "mysql://root:vMRGSikrOSdOSNIrDgMKotdVNUjSxPAF@shuttle.proxy.rlwy.net:25290/railway"

# 2. Format the URL for SQLAlchemy + PyMySQL
# SQLAlchemy needs the +pymysql driver specification
if RAW_URL.startswith("mysql://"):
    SQLALCHEMY_DATABASE_URL = RAW_URL.replace("mysql://", "mysql+pymysql://", 1)
else:
    SQLALCHEMY_DATABASE_URL = RAW_URL

# 3. Create the Engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True,
    pool_recycle=3600
)

# 4. Session Configuration
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Base class for our models
Base = declarative_base()

# 6. Dependency to get the DB session (to be used in FastAPI routes)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Quick Health Check to run during setup
if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print("✅ Success Connected to MySQL!")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
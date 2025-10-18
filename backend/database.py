from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://mugswap_user:mugswap_pass@localhost/mugswap_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

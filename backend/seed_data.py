from database import SessionLocal, engine
from models import Base, Mug, User
import hashlib

# Sample mug data with people's names
SAMPLE_MUGS = [
    {
        "name": "Emma",
        "description": "Coffee enthusiast who loves early morning walks and cozy bookshops. Always up for trying new cafes!",
        "image_url": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400",
    },
    {
        "name": "Liam",
        "description": "Outdoor adventurer and camping lover. Enjoys rustic vibes and mountain coffee by the campfire.",
        "image_url": "https://images.unsplash.com/photo-1514228742587-6b1558fcf93a?w=400",
    },
    {
        "name": "Sophia",
        "description": "Minimalist at heart with a love for sleek, modern design. Believes less is more in everything.",
        "image_url": "https://images.unsplash.com/photo-1506372023823-741d06319fd6?w=400",
    },
    {
        "name": "Mason",
        "description": "Artisan who appreciates handcrafted items and unique textures. Values authenticity and creativity.",
        "image_url": "https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=400",
    },
    {
        "name": "Olivia",
        "description": "Loves showcasing beautiful beverages and has an eye for transparency and clarity in life.",
        "image_url": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400",
    },
    {
        "name": "Noah",
        "description": "Vibrant personality who brings color and joy to everything. Believes life should be as bright as a sunset.",
        "image_url": "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=400",
    },
    {
        "name": "Ava",
        "description": "Classic cocktail enthusiast with a taste for traditional and authentic experiences. Style icon.",
        "image_url": "https://images.unsplash.com/photo-1517191297489-d6a58b69e02c?w=400",
    },
    {
        "name": "Ethan",
        "description": "Eco-conscious traveler who values sustainability and natural materials. Always on the move with purpose.",
        "image_url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400",
    },
    {
        "name": "Isabella",
        "description": "Elegant and refined with a love for delicate patterns and timeless beauty. Appreciates fine details.",
        "image_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400",
    },
    {
        "name": "Jacob",
        "description": "Tech-savvy professional who values efficiency and durability. Keeps things cool under pressure.",
        "image_url": "https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=400",
    },
]


def hash_password(password: str) -> str:
    """Hash password using SHA256 (same as in main.py)"""
    return hashlib.sha256(password.encode()).hexdigest()


def create_admin_user(db):
    """Create admin user for development purposes"""
    # Check if admin user already exists
    admin_user = db.query(User).filter(User.email == "admin@example.com").first()
    if admin_user:
        print("Admin user already exists. Skipping creation.")
        return

    # Create admin user
    admin_user = User(
        email="admin@example.com",
        name="Admin User",
        age=30,
        bio="Development admin user for testing purposes.",
        password_hash=hash_password("test"),
    )

    db.add(admin_user)
    print("✅ Created admin user (email: admin@example.com, password: test)")


def create_sample_data():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create session
    db = SessionLocal()

    try:
        # Create admin user for development
        create_admin_user(db)

        # Clear existing mugs to update to new format
        existing_mugs = db.query(Mug).count()
        if existing_mugs > 0:
            print(f"Clearing {existing_mugs} existing mugs to update to new format...")
            db.query(Mug).delete()
            db.commit()

        # Add sample mugs with new format
        for mug_data in SAMPLE_MUGS:
            mug = Mug(**mug_data)
            db.add(mug)

        db.commit()
        print(f"Successfully added {len(SAMPLE_MUGS)} sample mugs to the database!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()

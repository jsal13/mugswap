from database import SessionLocal
from sqlalchemy import text


def migrate_database():
    """Remove the color, size, material, and price columns from mugs table"""

    # Get a database session
    db = SessionLocal()

    try:
        # Drop the columns that are no longer needed
        print("Removing unused columns from mugs table...")

        # Check if columns exist before trying to drop them
        result = db.execute(
            text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'mugs' 
            AND column_name IN ('color', 'size', 'material', 'price')
        """)
        )

        existing_columns = [row[0] for row in result.fetchall()]

        for column in existing_columns:
            print(f"Dropping column: {column}")
            db.execute(text(f"ALTER TABLE mugs DROP COLUMN IF EXISTS {column}"))

        db.commit()
        print("Migration completed successfully!")

    except Exception as e:
        print(f"Migration failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    migrate_database()

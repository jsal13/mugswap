#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
while ! nc -z postgres 5432; do
  sleep 1
done

echo "PostgreSQL is ready! Running database migrations and seeding..."

# Run database migration to remove old columns
python migrate.py

# Create tables and seed data
python seed_data.py

echo "Starting FastAPI server..."
exec python main.py
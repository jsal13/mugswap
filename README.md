# Mugswap - Coffee Mug Tinder Clone

A fun Tinder-style application for coffee mugs! Swipe through different coffee mug photos, build your collection of favorites, and discover your perfect mug match.

## Features

- 🔐 **User Authentication** - Register and login to your personal account
- 👤 **Profile Management** - Manage your profile and view your statistics
- ☕ **Mug Swiping** - Swipe through coffee mug photos (like/pass)
- ❤️ **Match System** - View all the mugs you've liked
- 📊 **Statistics** - Track your swiping activity and preferences

## Technology Stack

- **Frontend**: Vue.js 3 with Vite
- **Backend**: Python FastAPI
- **Database**: PostgreSQL
- **Authentication**: JWT tokens
- **Styling**: CSS3 with modern design

## Quick Start

### Prerequisites

- Docker and Docker Compose (recommended)
- OR Node.js (v16+) and Python (v3.8+) for local development

### Option A: Docker Setup (Recommended)

#### Production Mode
**Start the complete application (frontend + backend + database):**
```bash
docker-compose up --build
```

This will:
- Start PostgreSQL database
- Build and start the FastAPI backend
- Build and start the Vue.js frontend with Nginx
- Automatically seed the database with sample mugs

**Access the application:**
- **Full Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

#### Development Mode (with hot reload)
**For frontend development with hot reload:**
```bash
docker-compose -f docker-compose.dev.yml up --build
```

This provides:
- Live reloading for frontend changes
- Direct backend API access
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000

### Option B: Local Development Setup

### Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- PostgreSQL (or Docker)

### 1. Database Setup

#### Using Docker (Recommended)
```bash
docker-compose up -d postgres
```

#### Local PostgreSQL
Create a database and user:
```sql
CREATE DATABASE mugswap_db;
CREATE USER mugswap_user WITH PASSWORD 'mugswap_pass';
GRANT ALL PRIVILEGES ON DATABASE mugswap_db TO mugswap_user;
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Set environment variables (optional)
export DATABASE_URL="postgresql://mugswap_user:mugswap_pass@localhost/mugswap_db"
export SECRET_KEY="your-secret-key-here"

# Start the API server
python main.py
```

The API will be available at `http://localhost:8000`

### 3. Seed Sample Data

```bash
cd backend
python seed_data.py
```

### 4. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:8080`

## Docker Management

### Useful Docker Commands

```bash
# Production: Start all services (frontend + backend + database)
docker-compose up --build

# Development: Start with frontend hot reload
docker-compose -f docker-compose.dev.yml up --build

# Start services in background
docker-compose up -d --build

# Stop all services
docker-compose down

# View logs
docker-compose logs frontend
docker-compose logs backend
docker-compose logs postgres

# Rebuild and restart specific service
docker-compose up --build frontend
docker-compose up --build backend

# Access container shell
docker-compose exec frontend sh
docker-compose exec backend bash

# Reset everything (remove volumes and data)
docker-compose down -v
```

## Project Structure

```
mugswap/
├── backend/              # Python FastAPI backend
│   ├── main.py          # Main FastAPI application
│   ├── models.py        # Database models and Pydantic schemas
│   ├── database.py      # Database configuration
│   ├── seed_data.py     # Sample mug data seeder
│   └── requirements.txt # Python dependencies
├── frontend/            # Vue.js frontend
│   ├── src/
│   │   ├── views/       # Vue components for pages
│   │   ├── stores/      # Pinia stores for state management
│   │   ├── App.vue      # Main App component
│   │   ├── router.js    # Vue Router configuration
│   │   └── style.css    # Global styles
│   ├── package.json     # Node.js dependencies
│   ├── vite.config.js   # Vite configuration
│   ├── Dockerfile       # Frontend Docker build
│   ├── nginx.conf       # Nginx configuration
│   └── .dockerignore    # Docker ignore file
├── database/            # Database scripts
│   └── init.sql         # Database initialization
├── docker-compose.yml       # Production Docker services
└── docker-compose.dev.yml   # Development Docker services
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user

### Mugs
- `GET /api/mugs` - Get mugs for swiping (excludes already swiped)
- `POST /api/swipe` - Record a swipe action

### User
- `GET /api/profile` - Get user profile
- `GET /api/matches` - Get user's liked mugs

## Development

### Adding New Mugs

Edit `backend/seed_data.py` and add new mug objects to the `SAMPLE_MUGS` list:

```python
{
    "name": "Your Mug Name",
    "description": "Description of the mug",
    "image_url": "https://example.com/image.jpg",
    "color": "Color",
    "size": "Size (oz)",
    "material": "Material",
    "price": "$XX.XX"
}
```

Then run the seeder again: `python seed_data.py`

### Customizing Styles

The main styles are in `frontend/src/style.css`. The design uses a gradient background and card-based layout for a modern look.

### Database Schema

The application uses three main tables:
- `users` - User accounts and profiles
- `mugs` - Coffee mug data
- `swipe_actions` - Records user swipe actions (like/pass)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and entertainment purposes. Mug images are sourced from Unsplash and are used under their license terms.

## Support

For questions or issues, please create an issue in the repository.

Happy mug swiping! ☕❤️
DROP DATABASE mugswap_db;
-- Create database and user
CREATE DATABASE mugswap_db;
CREATE USER mugswap_user WITH PASSWORD 'mugswap_pass';
GRANT ALL PRIVILEGES ON DATABASE mugswap_db TO mugswap_user;

-- Connect to the database
\c mugswap_db;

-- Grant schema permissions
GRANT ALL ON SCHEMA public TO mugswap_user;

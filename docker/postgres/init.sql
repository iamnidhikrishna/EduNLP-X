-- EduNLP-X Database Initialization
-- This script sets up the initial database configuration

-- Create database if it doesn't exist
-- (This is handled by the POSTGRES_DB environment variable in docker-compose)

-- Create necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search optimization
CREATE EXTENSION IF NOT EXISTS "unaccent"; -- For accent-insensitive search

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE edunlpx_db TO edunlpx_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO edunlpx_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO edunlpx_user;

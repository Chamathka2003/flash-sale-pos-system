#!/bin/bash

# Setup script for the Flash Sale POS System
# Run this script to set up the entire project

echo "=================================="
echo "Flash Sale POS System - Setup"
echo "=================================="

# Backend setup
echo ""
echo "Setting up Backend..."
cd backend

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create database (ensure MySQL is running)
echo "Creating database..."
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS assignment_db;"

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Backend setup complete!"
echo "To start the backend: python manage.py runserver"

# Frontend setup
echo ""
echo "Setting up Frontend..."
cd ../frontend

echo "Installing npm dependencies..."
npm install

echo "Frontend setup complete!"
echo "To start the frontend: npm start"

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Start backend: cd backend && python manage.py runserver"
echo "2. Start frontend: cd frontend && npm start"
echo "3. Populate data: cd backend && python populate_data.py"
echo "4. Run tests: cd backend && python load_test.py"

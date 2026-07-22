#!/usr/bin/env bash
set -e

echo "=== Initializing RouteAI Development Environment ==="

# Initialize Backend
echo "Setting up Python virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created backend/.env from .env.example"
fi
cd ..

# Initialize Frontend
echo "Setting up Frontend node packages..."
cd frontend
npm install
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created frontend/.env from .env.example"
fi
cd ..

echo "=== RouteAI Setup Complete! ==="

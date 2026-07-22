Write-Host "=== Initializing RouteAI Development Environment ===" -ForegroundColor Green

# Backend Setup
Write-Host "Setting up Python virtual environment..." -ForegroundColor Yellow
Set-Location -Path backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "Created backend/.env from .env.example" -ForegroundColor Cyan
}
Set-Location -Path ..

# Frontend Setup
Write-Host "Setting up Frontend npm packages..." -ForegroundColor Yellow
Set-Location -Path frontend
npm install
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "Created frontend/.env from .env.example" -ForegroundColor Cyan
}
Set-Location -Path ..

Write-Host "=== RouteAI Setup Complete! ===" -ForegroundColor Green

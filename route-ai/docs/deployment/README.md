# 🚀 Production Deployment Playbook

## Deployment Architecture
- **Frontend**: Deployed on **Vercel** with CDN distribution.
- **Backend Service**: Deployed on **Railway** container runtime.
- **Database**: Managed PostgreSQL instance on Railway.

## Deployment Steps

### 1. Database Provisioning (Railway)
1. Log into Railway console and create a new project.
2. Add a PostgreSQL database service.
3. Copy the internal and public connection strings (`DATABASE_URL`).

### 2. Backend Deployment (Railway)
1. Add a new service from GitHub repository targeting `backend/`.
2. Configure Environment Variables:
   - `DATABASE_URL`: Your Railway PostgreSQL connection string
   - `SECRET_KEY`: Long random string for JWT signatures
   - `GEMINI_API_KEY`: Your production Gemini API key
   - `CORS_ORIGINS`: `["https://your-vercel-app.vercel.app"]`
3. Railway automatically detects Python 3.11 and runs Uvicorn.

### 3. Frontend Deployment (Vercel)
1. Import GitHub project into Vercel console.
2. Select root directory: `frontend`.
3. Set environment variable: `VITE_API_BASE_URL=https://your-backend-railway-url.com/api/v1`.
4. Deploy!

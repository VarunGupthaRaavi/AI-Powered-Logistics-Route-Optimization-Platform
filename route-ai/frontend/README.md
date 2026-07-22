# 💻 RouteAI Frontend Client

The frontend application for **RouteAI** is an enterprise-grade operations dashboard designed for dispatchers, fleet supervisors, and logistics managers. Built with **React 18**, **Vite**, and **Tailwind CSS**, it offers high performance, dark-mode visual aesthetics, real-time map visualizations, and conversational AI interface widgets.

---

## 🛠️ Technology Stack

- **Core Framework**: React 18
- **Build Tool & Dev Server**: Vite 5
- **Styling & Design System**: Tailwind CSS 3 with custom enterprise logistics palette
- **Icons**: Lucide React
- **Routing**: React Router DOM 6
- **HTTP Client**: Axios with custom authorization interceptors
- **Utility Libraries**: `clsx`, `tailwind-merge`

---

## 📁 Source Directory Layout (`src/`)

```
src/
├── assets/          # Static branding images, icons, and SVG illustrations
├── components/      # Modular UI components grouped by feature domain
│   ├── common/      # Generic widgets (Header, Sidebar, SearchBars, Badges)
│   ├── dashboard/   # Live fleet metric cards, activity feeds, mini-maps
│   ├── delivery/    # Order status tables, delivery detail modals
│   ├── driver/      # Driver roster cards, performance metrics, availability toggles
│   ├── vehicle/     # Vehicle telemetry lists, fuel/battery level meters
│   ├── routes/      # Interactive route path visualizers, waypoint re-ordering
│   ├── analytics/   # Logistics KPI charts, fuel consumption & SLA graphs
│   ├── ai/          # Gemini AI prompt input bar, RAG response chat drawer
│   └── ui/          # Low-level primitive components (Buttons, Inputs, Modals, Cards)
│
├── layouts/         # Layout wrappers
│   ├── MainLayout.jsx  # Main application layout with Sidebar & Header
│   └── AuthLayout.jsx  # Centered card layout for Login & Registration
│
├── pages/           # View pages mapped to React Router routes
│   ├── auth/        # Login & Register views
│   ├── dashboard/   # Operations Dashboard
│   ├── deliveries/  # Deliveries Management
│   ├── drivers/     # Driver Fleet Roster
│   ├── vehicles/    # Vehicles Fleet Roster
│   ├── routes/      # Route Optimization & Dispatcher Map
│   ├── analytics/   # Analytics & KPI Reports
│   ├── ai/          # AI Logistics Assistant (Gemini)
│   └── settings/    # Platform Settings
│
├── context/         # React Context state providers (AuthContext)
├── hooks/           # Custom React hooks (useAuth, useRoutes, useDeliveries)
├── services/        # Client API integration services
├── api/             # Axios client instance with Bearer token interceptor
├── utils/           # Helper functions (date formatting, distance math)
├── constants/       # Global application constants and navigation links
├── routes/          # Central React Router setup (AppRoutes.jsx)
└── styles/          # Tailwind directives and custom CSS rules (index.css)
```

---

## 🚀 Local Development Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Ensure the API base URL matches your running FastAPI backend:
```ini
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=RouteAI
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_key
```

### 3. Start Development Server
```bash
npm run dev
```
Open your browser and navigate to `http://localhost:3000`.

### 4. Build for Production
To bundle static production assets into the `dist/` folder:
```bash
npm run build
```

To preview the built production bundle locally:
```bash
npm run preview
```

---

## 🎨 Styling Guidelines & Design System

The application uses a custom Tailwind theme configured in `tailwind.config.js`:
- **Dark Theme Palette**: Slate dark background (`#0f172a`), Card surface (`#1e293b`), Accent border (`#334155`).
- **Brand Colors**:
  - `brand-500` / `brand-600`: Sky blue primary brand accents (`#0284c7`, `#0369a1`).
  - `logistics-success`: Emerald green status indicators (`#10b981`).
  - `logistics-warning`: Amber warning indicators (`#f59e0b`).
  - `logistics-danger`: Rose red emergency/breakdown alerts (`#ef4444`).

All components should utilize existing utility tokens to maintain visual consistency across all view pages.

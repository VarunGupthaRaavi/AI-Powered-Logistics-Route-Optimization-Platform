# 🐘 Database Schema & ORM Model Specs

## Database Engine
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0 (Declarative Base)
- **Migrations**: Alembic

## Core Entities
1. `users`: System accounts (Dispatchers, Fleet Supervisors, Administrators).
2. `drivers`: Driver roster, license information, status (`available`, `on_route`, `off_duty`).
3. `vehicles`: Fleet vehicles, license plate, maximum weight capacity (kg), fuel/battery metrics.
4. `deliveries`: Packages, delivery coordinates, customer details, SLA time windows.
5. `routes`: Generated optimized route paths, assigned vehicle/driver, waypoints list, total distance.

## Indexing Strategy
- B-Tree indexes on all Foreign Keys (`driver_id`, `vehicle_id`, `route_id`).
- Unique composite index on `(license_plate)` and `(email)`.
- Index on `deliveries(status, created_at)` for fast operational queue filtering.

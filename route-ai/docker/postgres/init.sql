-- PostgreSQL Initialization Script for RouteAI Platform
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Setup default database schema version comment
COMMENT ON DATABASE routeai_db IS 'RouteAI Logistics Platform Production Database';

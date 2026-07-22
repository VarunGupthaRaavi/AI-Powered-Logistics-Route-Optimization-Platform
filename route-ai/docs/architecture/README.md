# 🏛️ System Architecture Specification

## Overview
RouteAI utilizes an enterprise multi-tier architecture designed for continuous high throughput, real-time telemetry processing, and fast AI inference response times.

## Architectural Principles
1. **Decoupled Client & Server**: React single-page dashboard application communicates exclusively via REST APIs.
2. **Asynchronous I/O**: FastAPI with Python `asyncio` for non-blocking database queries and external AI calls.
3. **Repository Abstraction Pattern**: Services consume generic data repositories to maintain strict decoupling from ORM specifics.
4. **Stateless Authentication**: JWT tokens enable horizontal scaling without session replication bottlenecks.
5. **AI Subsystem Isolation**: VRP solvers and Gemini API calls are isolated into standalone service engines under `app/ai/`.

# 🤖 AI & Google Gemini Integration Deep Dive

## Overview
RouteAI leverages **Google Gemini 2.5 API** for dynamic routing intelligence, constraint reasoning, natural language dispatching, and RAG document querying.

## AI Modules Overview

### 1. `route_optimizer/`
Solves Vehicle Routing Problems with time windows (VRPTW). Calculates distance matrices and feeds constraints into Gemini model for optimal order sequencing.

### 2. `eta_prediction/`
Predicts real-world travel durations by factoring in historical route leg completion times, driver experience profiles, and current traffic conditions.

### 3. `dynamic_routing/`
Triggers immediate route recalculation when a driver encounters unexpected delays or vehicle malfunctions mid-route.

### 4. `multi_agent/`
Implements an autonomous agent loop where driver agents negotiate package handoffs based on geographical proximity and capacity.

### 5. `rag/`
Uses vector embeddings over logistics operating procedure manuals, allowing dispatchers to ask questions such as:
*"What is the standard procedure when a customer is not available for a signature delivery?"*

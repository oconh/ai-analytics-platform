# Project Analytics Platform MVP

## Business Requirements

This project is building an end-to-end analytics platform.

Key features:

* A data generator produces synthetic business events continuously
* Events are stored in PostgreSQL
* A FastAPI backend exposes analytics over the event data
* An Angular frontend displays analytics dashboards
* The system supports multiple analytics views (revenue, product activity, event tracking)

For the MVP:

* Single local environment setup
* Single PostgreSQL instance
* Single backend API service
* Single Angular frontend application
* No authentication required yet

The system runs locally via Docker in future iterations.

---

## Technical Decisions

* Angular frontend for analytics dashboard UI
* Python FastAPI backend for API layer
* PostgreSQL for persistent event storage
* Python event generator for synthetic data streaming
* REST APIs used between frontend and backend
* Local-first development (no cloud dependency in MVP)

Future extensions may include Kafka, Kubernetes, and AI-based analytics services.

---

## Starting Point

* A Python event generator already produces and stores events in PostgreSQL
* FastAPI backend exposes initial analytics endpoints
* Angular frontend will be used for dashboards and visualisation (in development)

Frontend and backend are currently being integrated into a unified full-stack application.

---

## Project Structure

* `services/generator/` – Event generation and ingestion
* `services/analytics/` – SQL-based analytics queries
* `services/api/` – FastAPI backend services
* `frontend/` – Angular dashboard application
* `k8s/` – Kubernetes manifests (future)
* `tests/` – Automated tests
* `docs/` – Project documentation and planning

---

## Data Model

* PostgreSQL is the source of truth
* Events represent user/product activity
* Analytics are computed via SQL queries
* Python is used for orchestration and API exposure only

---

## API Layer

FastAPI provides the interface between frontend and database.

Core endpoints:

* `/events/count`
* `/analytics/top-products`
* `/analytics/revenue`

Guidelines:

* Return JSON only
* Keep endpoints simple and explicit
* Do not expose database internals to the frontend

---

## Frontend (Angular)

The Angular frontend is a dashboard for analytics visualization.

Responsibilities:

* Display analytics data from FastAPI
* Show tables and charts for insights
* Provide clean separation between UI and backend logic

Communication:

* HTTP calls to FastAPI only
* No direct database access

Planned views:

* Revenue dashboard
* Product performance view
* Event monitoring view

---

## Configuration

* Use environment variables for configuration
* Never hardcode secrets or credentials
* Store local values in `.env`
* `.env` must never be committed to version control

---

## Dependencies

* Python virtual environment required for backend
* Node.js required for Angular frontend
* Dependencies are split between frontend and backend environments

---

## Testing

* Backend: pytest
* Frontend: Angular testing tools
* Focus on correctness of analytics and API responses

---

## Git Workflow

* Commit frequently with clear messages
* Keep backend and frontend changes separate where possible
* Ensure system remains runnable after every commit

Example commit types:

* `feat: add analytics endpoint`
* `feat: add angular dashboard integration`
* `fix: resolve postgres query issue`

---

## Agent Instructions

When working in this repository:

1. Preserve existing functionality
2. Avoid unnecessary complexity or abstraction
3. Ensure backend and frontend remain loosely coupled
4. Prefer simple, explicit solutions over clever implementations
5. Validate changes against actual runtime behavior before committing
6. Update documentation when system behaviour changes
7. Identify root cause before applying fixes — do not guess

---

## Long-Term Vision

This project is intended to evolve into a production-grade analytics platform demonstrating:

* Python backend engineering
* Data pipeline design
* SQL analytics systems
* Angular frontend development
* Containerization and Docker workflows
* Kubernetes deployment (future)
* AI-assisted analytics and insights (future extension)

The system should remain simple at MVP stage but architecturally capable of scaling into a modern cloud-native data platform.

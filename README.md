A Dockerized full‑stack To‑Do app with:
- Flask API (CRUD + due‑dates, priorities, completed toggle)
- SQLite persistence
- HTTP Basic Auth on mutating endpoints
- Nginx‑served frontend (vanilla JS + Tailwind)
- CI via GitHub Actions (pytest)

## Usage

```bash
# Build & start
docker-compose up --build -d

# Frontend UI
open http://localhost:8002

# API (unauthenticated GET)
curl http://localhost:5001/tasks

# Authenticated POST
curl -u admin:secret123 -X POST http://localhost:5001/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Example","due_date":"2025-07-30","priority":2}'

# Toggle & delete
curl -u admin:secret123 -X PUT    http://localhost:5001/tasks/1/toggle
curl -u admin:secret123 -X DELETE http://localhost:5001/tasks/1
CI Badge


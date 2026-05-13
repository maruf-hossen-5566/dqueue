# DQueue 🚀
A distributed task queue for Python backends using PostgreSQL as the message broker. Built to handle asynchronous background workloads with fault tolerance and atomic job processing.

## 📁 Project Structure
- app/ — FastAPI application and core logic
- worker/ — Standalone worker process for task execution
- alembic/ — Database schema migrations
- frontend/ — Task monitoring UI

## Quick Start
### 1. Install Dependencies (using uv):
```bash
uv sync
```
or
```base
pip install -r requirements.txt
```

### 2. DB Setup:
```bash
docker-compose up -d
alembic upgrade head
```

### 3. Run Services:
```bash
# Terminal 1
uvicorn app.main:app

# Terminal 2
python -m worker.main
```

## 🛠️ Tech Stack
- Backend: FastAPI, SQLAlchemy (PostgreSQL)
- Tooling: uv (dependency management), Docker
- Migrations: Alembic

---

Built by [SM Maruf Hossen](https://github.com/maruf-hossen-5566)
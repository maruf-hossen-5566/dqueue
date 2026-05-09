# backend/Dockerfile

FROM python:3.11-slim

COPY . /app
WORKDIR /app

# Install FastAPI, uvicorn, and psycopg2 (for PostgreSQL + SQLAlchemy)
RUN pip install "fastapi[standard]" uvicorn psycopg2-binary psycopg

# If you have requirements.txt, install that too:
RUN pip install -r requirements.txt

# Copy the startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh  # Make the script executable

CMD ["/app/start.sh"]
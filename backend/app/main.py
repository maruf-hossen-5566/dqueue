from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.job import router as job_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

app = FastAPI(root_path="/api")

# This line must be added to create all the tables
Base.metadata.create_all(bind=engine)

origins = settings.ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(job_router, prefix="/jobs", tags=["Jobs"])


@app.get("/")
def root():
    return {"message": "Hello World!"}

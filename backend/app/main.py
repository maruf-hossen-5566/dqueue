from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.job import router as job_router

app = FastAPI(root_path="/api")

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:4173",
]

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

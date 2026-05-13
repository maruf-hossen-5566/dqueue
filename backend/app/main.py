from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

import app.models
from app.api.job import limiter
from app.api.job import router as job_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

app = FastAPI(root_path="/api")
app.state.limiter = limiter

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


@app.exception_handler(RateLimitExceeded)
async def rate_imit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    if request.url.path == "/api/jobs/" and request.method == "POST":
        message = "You've reached your daily limit of 10 tasks. Try again in 24 hours."
    else:
        message = "Too many requests. Try again later."
    return JSONResponse(
        status_code=429,
        content={"detail": message},
    )


@app.get("/")
def root(request: Request):
    return {"message": "Hello World!"}

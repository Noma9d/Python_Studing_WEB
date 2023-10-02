from fastapi import FastAPI
from src.routes import contacts, auth, users
from fastapi.middleware.cors import CORSMiddleware
from src.config.config import settings
from fastapi_limiter import FastAPILimiter
import redis

app = FastAPI()

app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.get("/")
async def read_root():
    """
    Root route handler.
    Returns:
        dict: JSON object with message.

    """
    return {"Message": "This is a root of project"}


origins = ["http://localhost:8000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """
    A function executed when the application starts.
    Initializes FastAPILimiter using Redis.
    Raises:
        Exception: If unable to connect to Redis.
    """
    r = await redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        db=0,
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(r)

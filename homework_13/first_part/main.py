from fastapi import FastAPI
from src.routes import contacts, auth, users
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.get("/")
async def read_root():
    return {"Message": "This is a root of project"}


origins = ["http://localhost:8000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

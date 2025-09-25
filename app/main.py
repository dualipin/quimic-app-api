from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi import FastAPI
from app.core.database import Base, engine
from app.core.config import get_settings
from app.api.v1.endpoints import router as api_v1_router


Base.metadata.create_all(bind=engine)
MAINDIR = Path(__file__).resolve().parent.parent


app = FastAPI()

settings = get_settings()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/api")

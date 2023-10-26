import os
import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from .answer.routers import router as answer_router
from .internal.routers import router as internal_router
from .user.routers import router as user_router

app = FastAPI()

origins = str(os.environ.get("CORS_ALLOW_ORIGINS")).split(",") if os.environ.get("CORS_ALLOW_ORIGINS") else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    pass


app.include_router(answer_router)
app.include_router(internal_router)
app.include_router(user_router)

uvicorn.Config(app, log_level="debug", access_log=True)

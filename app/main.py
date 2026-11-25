from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.topic import router as topic_router
from app.routers.hooks import router as hooks_router
from app.routers.outline import router as outline_router
from app.routers.script import router as script_router
from app.routers.visuals import router as visuals_router
from app.routers.description import router as description_router
from app.routers.regeneration import router as regeneration_router
from app.routers.saved_scripts import router as saved_scripts_router

app = FastAPI(
    title="YouTube Script Assistant",
    description="AI-powered YouTube content generation application",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(topic_router)
app.include_router(hooks_router)
app.include_router(outline_router)
app.include_router(script_router)
app.include_router(visuals_router)
app.include_router(description_router)
app.include_router(regeneration_router)
app.include_router(saved_scripts_router)


@app.get("/")
def home():
    return {"message": "Welcome to YouTube Script Assistant"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "YouTube Script Assistant",
    }
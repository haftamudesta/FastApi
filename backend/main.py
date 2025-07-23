from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from routers import story, job
from db.database import create_tables

create_tables()

app = FastAPI(
    title="Choose your own adventure Game API",
    description="Api to generate coole stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redocs"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(story.router, prefix=settings.APP_PREFIX)
app.include_router(job.router, prefix=settings.APP_PREFIX)


@app.get("/")
def home():
    return {"message": "Hello FASTAPI"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

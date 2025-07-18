from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Choose your own adventure Game API",
    description="Api to generate coole stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redocs"
)
app.add_middleware(
    CORSMiddleware
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, "main:app", host="0.0.0.0", port=8000, reload=True)

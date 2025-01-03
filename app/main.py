from fastapi import FastAPI

app = FastAPI(title="Career Loop API")


@app.get("/")
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Career Loop API"}


@app.get("/health")
def read_health():
    """A health check endpoint."""
    return {"status": "ok"}

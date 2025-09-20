from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Application",
    description="A FastAPI application with SQLModel integration",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application"}
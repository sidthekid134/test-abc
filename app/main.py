from fastapi import FastAPI

app = FastAPI(title="FastAPI Application")

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Application"}
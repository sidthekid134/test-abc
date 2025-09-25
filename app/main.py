from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger("task_management")

from app.models.base import create_db_and_tables
from app.routers import task

app = FastAPI(
    title="Task Management API",
    description="A simple task management API",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(task.router, prefix="/api", tags=["tasks"])

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    error_trace = traceback.format_exc()
    
    # Log the full error for server-side debugging
    print(f"ERROR: {str(exc)}\n{error_trace}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error occurred", "error_id": str(datetime.utcnow().timestamp())},
    )


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


from sqlmodel.exceptions import SQLModelError
@app.exception_handler(SQLModelError)
async def sqlmodel_exception_handler(request: Request, exc: SQLModelError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": f"Database error: {str(exc)}"},
    )


from datetime import datetime
from fastapi.exceptions import RequestValidationError
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_messages = []
    
    for error in errors:
        loc = " -> ".join([str(x) for x in error["loc"]])
        msg = error["msg"]
        error_messages.append(f"{loc}: {msg}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": error_messages},
    )

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {
        "message": "Task Management API",
        "docs": "/docs",
        "redoc": "/redoc",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
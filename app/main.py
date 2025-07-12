from fastapi import FastAPI
from app.api.routes_presentation import router as presentation_router
from app.utils.limiter import limiter, rate_limit_exceeded_handler
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title="Slide Generator API", version="1.0")
app.state.limiter = limiter

# Register exception handlers
app.add_exception_handler(429, rate_limit_exceeded_handler)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(Exception)
async def internal_error_handler(request, exc):
    return JSONResponse(status_code=500, content={"error": str(exc)})

# Mount routers
app.include_router(presentation_router, prefix="/api/v1/presentations")

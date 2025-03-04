from fastapi import FastAPI
from app.api.user import router as user_router  # import the router with user routes
from app.api.clients import router as clients_router  # import the router with client routes
from app.api.category import router as category_router  # import the router with category routes
from app.api.subcategory import router as subcategory_router  # import the router with subcategory routes
from app.api.invouchers import router as invouchers_router  # import the router with subcategory routes
from app.api.products import router as products_router  # import the router with product routes
from app.api.outvoucher import router as outvoucher_router  # import the router with outvoucher routes
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles 
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()
# Middleware to allow larger file uploads
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"]
)
app.add_middleware(
    GZipMiddleware, minimum_size=1000  # Optional: Enable compression
)
# Allow CORS for specific origins (localhost:3000, etc.)
origins = [
    "http://localhost:3000",  # Local development frontend
    "https://www.panvik.in",  # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers for different APIs
app.include_router(user_router)
app.include_router(clients_router)
app.include_router(subcategory_router)
app.include_router(products_router)
app.include_router(category_router)
app.include_router(invouchers_router)
app.include_router(outvoucher_router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
# Increase max request size
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class MaxUploadSizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        max_size = 3 * 1024 * 1024  # 🔥 Increase to 10MB (Change as needed)
        if request.headers.get("content-length") and int(request.headers["content-length"]) > max_size:
            return Response("413 Request Entity Too Large", status_code=413)
        return await call_next(request)

app.add_middleware(MaxUploadSizeMiddleware)

@app.get("/")
def read_root():
    return {"message": "Welcome to user API"}

# Run with Uvicorn if this script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)  # Run on port 80 for production

from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy.orm import Session

# ✅ API routers
from app.api.user import router as user_router
from app.api.clients import router as clients_router
from app.api.category import router as category_router
from app.api.subcategory import router as subcategory_router
from app.api.invouchers import router as invouchers_router
from app.api.products import router as products_router
from app.api.outvouchers import router as outvouchers_router
from app.api.quotation import router as quotations_router
from app.api.SalesOrder import router as sales_router
from app.products_import import router as product_import_router
from app.api.wooproducts import router as woo_router
from app.api.csv_upload import upload_csv
from app.api.inventory import router as inventory_router
from app.api.switches_quotation import router as switches_quotation
from database import get_db_connection

app = FastAPI()

# ✅ Add middleware for large file uploads
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(GZipMiddleware, minimum_size=1000)

# ✅ Add CORS Middleware (fixes the CORS issue you're facing)
origins = [
    "http://localhost:3000",
    "https://panvik.in",
    "https://www.panvik.in",
    "https://api.panvic.in",  # ✅ ADD THIS
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Log origin middleware (for debugging)
@app.middleware("http")
async def log_origin(request: Request, call_next):
    print("🔍 Incoming Origin:", request.headers.get("origin"))
    return await call_next(request)

# ✅ Middleware for upload size
class MaxUploadSizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        max_size = 10 * 1024 * 1024  # 10 MB
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > max_size:
            return Response("413 Request Entity Too Large", status_code=413)
        return await call_next(request)

app.add_middleware(MaxUploadSizeMiddleware)

# ✅ Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ✅ Base route
@app.get("/")
def read_root():
    return {"message": "Welcome to user API"}

# ✅ CSV Upload route
@app.post("/upload-csv/")
async def upload_csv_endpoint(file: UploadFile = File(...), db: Session = Depends(get_db_connection)):
    return upload_csv(file, db)

# ✅ Register all routers
app.include_router(user_router)
app.include_router(clients_router)
app.include_router(category_router)
app.include_router(subcategory_router)
app.include_router(invouchers_router)
app.include_router(products_router)
app.include_router(outvouchers_router)
app.include_router(quotations_router)
app.include_router(product_import_router)
app.include_router(sales_router)
app.include_router(woo_router)
app.include_router(inventory_router)
app.include_router(switches_quotation)

# ✅ Run app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)

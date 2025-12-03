from fastapi import FastAPI, Depends, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from sqlalchemy.orm import Session

# Routers
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
from app.api.products_router import router as products_update_router
from app.api.purchaseorder_api import router as purchaseorder_router
from app.api.catalogue_routes import router as catalogue_routes
from app.api.csv_routers import router as csv_routers

# Create app
app = FastAPI()

# ✅ Set allowed origins including frontend and API domains
origins = [
    "http://localhost:3000",
    "https://panvik.in",
    "https://www.panvik.in",
    "https://api.panvic.in"
]

# ✅ Apply CORS middleware before anything else
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Log incoming request origin (for debugging CORS issues)
@app.middleware("http")
async def log_origin(request: Request, call_next):
    print("🔍 Request from Origin:", request.headers.get("origin"))
    return await call_next(request)

# ✅ Trusted Host Middleware (accept all for now)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# ✅ Enable GZIP compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# ✅ Upload size middleware (10MB limit)
class MaxUploadSizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        max_size = 10 * 1024 * 1024  # 10 MB
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > max_size:
            return Response("413 Request Entity Too Large", status_code=413)
        return await call_next(request)

app.add_middleware(MaxUploadSizeMiddleware)

# ✅ Mount static folder
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ✅ Root route
@app.get("/")
def read_root():
    return {"Hello": "World"}

# ✅ Upload CSV route
@app.post("/upload-csv/")
async def upload_csv_endpoint(file: UploadFile = File(...), db: Session = Depends(get_db_connection)):
    return upload_csv(file, db)

# ✅ Include all routers
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
app.include_router(products_update_router)
app.include_router(purchaseorder_router)
app.include_router(catalogue_routes)
app.include_router(csv_routers)

# ✅ Run app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)

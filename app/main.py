from fastapi import (
    FastAPI,
    Depends,
    UploadFile,
    File,
    Request,
)
from fastapi.middleware.cors import (
    CORSMiddleware,
)
from fastapi.middleware.trustedhost import (
    TrustedHostMiddleware,
)
from fastapi.middleware.gzip import (
    GZipMiddleware,
)
from fastapi.staticfiles import (
    StaticFiles,
)
from starlette.middleware.base import (
    BaseHTTPMiddleware,
)
from starlette.responses import (
    Response,
)
from sqlalchemy.orm import Session

# =========================================
# IMPORT ROUTERS
# =========================================

from app.api.user import router as user_router
from app.api.clients import router as clients_router
from app.api.category import router as category_router
from app.api.subcategory import router as subcategory_router
from app.api.invouchers import router as invouchers_router
from app.api.products import router as products_router
from app.api.outvouchers import router as outvouchers_router
from app.api.quotation import router as quotations_router
from app.api.SalesOrder import router as sales_router
from app.products_import import (
    router as product_import_router,
)
from app.api.wooproducts import (
    router as woo_router,
)
from app.api.inventory import (
    router as inventory_router,
)
from app.api.switch_quotation_routes import (
    router as switches_quotation,
)
from app.api.products_router import (
    router as products_update_router,
)
from app.api.purchaseorder_api import (
    router as purchaseorder_router,
)
from app.api.catalogue_routes import (
    router as catalogue_routes,
)
from app.api.csv_routers import (
    router as csv_routers,
)
from app.api.csv_upload import upload_csv
from app.api.brand_routes import (
    router as brand_router,
)

from app.api.arch_register_routes import (
    router as arch_register_router,
)

from app.api.arch_auth_routes import (
    router as arch_auth_router,
)

from database import get_db_connection

# =========================================
# CREATE FASTAPI APP
# =========================================

app = FastAPI(
    title="Panvic API"
)

# =========================================
# CORS ORIGINS
# =========================================

origins = [
    # LOCALHOST
    "http://localhost:3000",
    "http://127.0.0.1:3000",

    # PANVIK
    "https://panvik.in",
    "https://www.panvik.in",

    # PANVIC API
    "https://api.panvic.in",

    # ARCH APP
    "https://archapp-blush.vercel.app",
    "https://www.archapp-blush.vercel.app",

    # VERCEL PREVIEW URL SUPPORT
    "https://*.vercel.app",
]

# =========================================
# CORS MIDDLEWARE
# MUST BE FIRST
# =========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=origins,

    # OPTIONAL REGEX SUPPORT
    allow_origin_regex=r"https://.*\.vercel\.app",

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ],

    expose_headers=[
        "*"
    ],
)

# =========================================
# TRUSTED HOST
# =========================================

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "*"
    ]
)

# =========================================
# GZIP
# =========================================

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000
)

# =========================================
# MAX UPLOAD SIZE
# =========================================

class MaxUploadSizeMiddleware(
    BaseHTTPMiddleware
):
    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        max_size = (
            10 * 1024 * 1024
        )  # 10MB

        content_length = (
            request.headers.get(
                "content-length"
            )
        )

        if (
            content_length
            and int(content_length)
            > max_size
        ):
            return Response(
                content="413 Request Entity Too Large",
                status_code=413,
            )

        response = await call_next(
            request
        )

        return response

app.add_middleware(
    MaxUploadSizeMiddleware
)

# =========================================
# STATIC FILES
# =========================================

app.mount(
    "/qr_codes",
    StaticFiles(directory="qr_codes"),
    name="qr_codes",
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)

# =========================================
# ROOT ROUTE
# =========================================

@app.get("/")
def read_root():
    return {
        "message":
        "Panvic API running"
    }

# =========================================
# HEALTH CHECK
# =========================================

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }

# =========================================
# PREFLIGHT OPTIONS FIX
# =========================================

@app.options(
    "/{full_path:path}"
)
async def options_handler(
    full_path: str
):
    return {
        "message": "OK"
    }

# =========================================
# CSV UPLOAD
# =========================================

@app.post("/upload-csv/")
async def upload_csv_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(
        get_db_connection
    )
):
    return upload_csv(file, db)

# =========================================
# INCLUDE ROUTERS
# =========================================

routers = [
    user_router,
    clients_router,
    category_router,
    subcategory_router,
    invouchers_router,
    products_router,
    outvouchers_router,
    quotations_router,
    product_import_router,
    sales_router,
    woo_router,
    inventory_router,
    switches_quotation,
    products_update_router,
    purchaseorder_router,
    catalogue_routes,
    csv_routers,
    brand_router,
    arch_register_router,
    arch_auth_router,
]

for r in routers:
    app.include_router(r)

# =========================================
# START SERVER
# =========================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
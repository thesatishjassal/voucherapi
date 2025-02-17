from fastapi import FastAPI
from app.api.user import router as user_router  # import the router with user routes
from app.api.clients import router as cliets_router  # import the router with user routes
from app.api.category import router as category_router  # import the router with user routes
from app.api.subcategory import router as subcategory_router  # import the router with user routes
from app.api.products import router as products_router  # import the router with user routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for specific origin (localhost:3000)
origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:5500",  # ✅ Allow this origin
    "https://vocherapp.vercel.app",
    "https://147.93.107.232:5500"
]


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Registering the router with a prefix (optional)
app.include_router(user_router)
app.include_router(user_router)
app.include_router(cliets_router)
app.include_router(subcategory_router)
app.include_router(products_router)
app.include_router(category_router)

@app.get("/")
def read_root():
    return {"message": "welcome to user API"}

from fastapi import FastAPI
from app.api.user import router as user_router  # import the router with user routes
from app.api.clients import router as clients_router  # import the router with client routes
from app.api.category import router as category_router  # import the router with category routes
from app.api.subcategory import router as subcategory_router  # import the router with subcategory routes
from app.api.products import router as products_router  # import the router with product routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for specific origins (localhost:3000, etc.)
origins = [
    "http://localhost:3000",  # Local development frontend
    "https://www.panvic.in",  # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ✅ Make sure this includes "https://www.panvic.in"
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # ✅ Allow all headers
)

# Register routers for different APIs
app.include_router(user_router)
app.include_router(clients_router)
app.include_router(subcategory_router)
app.include_router(products_router)
app.include_router(category_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to user API"}

# Run with Uvicorn if this script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)  # Run on port 80 for production

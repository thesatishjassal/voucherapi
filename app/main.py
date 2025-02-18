from fastapi import FastAPI
from app.api.user import router as user_router
from app.api.clients import router as clients_router
from app.api.category import router as category_router
from app.api.subcategory import router as subcategory_router
from app.api.products import router as products_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for specific origins (localhost:3000, etc.)
origins = [
    "http://localhost:3000",  # Local development frontend
    "https://vocherapp.vercel.app",  # Your actual frontend URL
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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

@app.get("/")
def read_root():
    return {"message": "Welcome to user API"}

# Run with Uvicorn if this script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5500)  # Correct host format
    # uvicorn.run(app, host="127.0.0.1", port=5500)  # Correct host format

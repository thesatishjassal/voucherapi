from fastapi import FastAPI
from app.api.user import router as user_router  # import the router with user routes
from app.api.clients import router as cliets_router  # import the router with user routes
from app.api.category import router as category_router  # import the router with user routes
from app.api.subcategory import router as subcategory_router  # import the router with user routes

app = FastAPI()

# Registering the router with a prefix (optional)
app.include_router(user_router)
app.include_router(user_router)
app.include_router(cliets_router)
app.include_router(subcategory_router)

@app.get("/")
def read_root():
    return {"message": "welcome to user API"}

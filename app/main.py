from fastapi import FastAPI
from app.routes.user import router as user_router  # import the router with user routes

app = FastAPI()

# Registering the router with a prefix (optional)
app.include_router(user_router)



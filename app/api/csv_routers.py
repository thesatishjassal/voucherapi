from fastapi import APIRouter
from app.controllers.wipro_artisa import csv_controller

router = APIRouter()
router.include_router(csv_controller)

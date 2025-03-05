# app/models/__init__.py
from app.models.clients import Client
from app.models.invoucher import Invoucher
from app.models.outvoucher import Outvoucher
from app.models.outvoucher_item import OutvoucherItem
from app.models.products import Products
from base import Base


# from app.models.user import User  # Assuming this existsfrom .base import Base  # Base should be imported
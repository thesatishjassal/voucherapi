# app/models/__init__.py
from app.models.clients import Client
from app.models.products import Products
from app.models.invoucher import Invoucher
from app.models.invoucher_item import InvoucherItem
from base import Base
# from app.models.user import User  # Assuming this existsfrom .base import Base  # Base should be imported
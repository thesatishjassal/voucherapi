import os
from dotenv import load_dotenv

load_dotenv()

# Get database credentials from environment variables
DB_HOST = os.getenv("DATABASE_HOST")
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_NAME = os.getenv("DATABASE_NAME")
SB_URL = os.getenv("SUPABASE_URL")
SB_APIKEY = os.getenv("SUPABASE_API_KEY")
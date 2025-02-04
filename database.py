import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SB_URL = os.getenv("SUPABASE_URL")
SB_APIKEY = os.getenv("SUPABASE_API_KEY")

def get_db_connection():
    try:
        connection: Client = create_client(SB_URL, SB_APIKEY)
        print("Supabase connection successful!")
        return connection
    except Exception as e:
        print(f"Supabase Error: {e}")
        return None
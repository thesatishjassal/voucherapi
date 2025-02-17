from app.main import app  # make sure to import the app from main.py (or your actual file)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5500)
import pandas as pd
from pathlib import Path

class CSVService:

    @staticmethod
    async def read_uploaded_csv(file):
        df = pd.read_csv(file.file)
        return df.to_dict(orient="records")

    @staticmethod
    async def read_csv_from_disk(filename: str):
        file_path = Path(__file__).resolve().parent.parent / "data" / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"File {filename} not found in /data folder")

        df = pd.read_csv(file_path)
        return df.to_dict(orient="records")

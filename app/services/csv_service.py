import pandas as pd
from app.utils.file_reader import FileReader

class CSVService:
    
    @staticmethod
    def read_csv(file):
        df = FileReader.load_csv(file)
        return df.to_dict(orient="records")

import pandas as pd

class CSVService:
    
    @staticmethod
    async def read_csv(file):
        df = pd.read_csv(file.file)
        return df.to_dict(orient="records")

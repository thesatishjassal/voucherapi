import pandas as pd
from io import BytesIO

def parse_excel(file_bytes):
    df = pd.read_excel(BytesIO(file_bytes))
    products = df.to_dict(orient="records")
    return products

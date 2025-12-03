import pandas as pd

class FileReader:

    @staticmethod
    def load_csv(file):
        try:
            df = pd.read_csv(file.file)
            return df
        except Exception as e:
            print("CSV Error:", e)
            raise e

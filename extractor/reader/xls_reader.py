import pandas as pd
import io

class XlsReader:
    def get_json_data(self, file):
        file_stream = io.BytesIO(file.read())  # Convert file to memory stream
        df = pd.read_excel(file_stream, engine="xlrd")
        df = df.dropna(how="all")
        df = df.fillna('')
        data = df.values.tolist()
        return data
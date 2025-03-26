import pandas as pd


class TableReader:
    def __init__(self, columns=[]):
        self.columns = columns

    def get_json_data(self, file):
        df = pd.read_csv(file, on_bad_lines="warn", delimiter="\t", names=self.columns, skip_blank_lines=True)
        df = df.fillna("")
        data = df.values.tolist()
        return data

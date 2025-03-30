import json
from datetime import datetime

columns = [
    "Tran Date",
    "Chq No",
    "Particulars",
    "Debit",
    "Credit",
    "Balance",
    "Init.\nBr",
]

SKIP_PATTERN = "OPENING BALANCE"

START_PATTERN = json.dumps(columns)

END_PATTERN = "TRANSACTION TOTAL"


class AxisPdfAccountStatementExtractorV1:
    def get_transactions(self, json_data):
        transactions = []
        start = False
        for row in json_data:
            if json.dumps(row) == START_PATTERN:
                start = True
                continue
            if not start:
                continue
            if SKIP_PATTERN in json.dumps(row):
                continue
            if END_PATTERN in json.dumps(row):
                break
            transaction = {}
            for i in range(len(columns)):
                transaction[columns[i]] = row[i]
            transactions.append(transaction)
            transaction["Date"] = datetime.strptime(transaction["Tran Date"], "%d-%m-%Y").strftime("%Y-%m-%d")
        return transactions

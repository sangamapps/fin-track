import json
from datetime import datetime

columns = [
    "Date",
    "Narration",
    "Chq./Ref.No.",
    "Value Dt",
    "Withdrawal Amt.",
    "Deposit Amt.",
    "Closing Balance",
]

SKIP_PATTERN = "********"

START_PATTERN = json.dumps(columns)

END_PATTERN = "STATEMENT SUMMARY"


class HdfcXlsAccountStatementExtractorV1:
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
            transaction["Date"] = datetime.strptime(transaction["Date"], "%d/%m/%y").strftime("%Y-%m-%d")
            transactions.append(transaction)
        return transactions

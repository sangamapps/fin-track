import json
from datetime import datetime

columns = [
    "Txn Date",
    "Value Date",
    "Description",
    "Ref No./Cheque No.",
    "Debit",
    "Credit",
    "Balance"
]

START_PATTERN = "End Date"

END_PATTERN = "**This is a computer generated statement and does not require a signature"

class SbiXlsAccountStatementExtractorV1:
    def get_transactions(self, json_data):
        transactions = []
        start = False
        for row in json_data:
            if (START_PATTERN in json.dumps(row)):
                start = True
                continue
            if not start:
                continue
            if (END_PATTERN in json.dumps(row)):
                break
            transaction = {}
            for i in range(len(columns)):
                transaction[columns[i]] = row[i]
            transactions.append(transaction)
        return transactions
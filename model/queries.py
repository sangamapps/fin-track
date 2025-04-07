ACCOUNTS_LOOKUP_QUERY = {
    "$lookup": {
        "from": "transactions",
        "let": {"accountId": "$_id"},
        "pipeline": [
            {"$addFields": {"accountObjectId": {"$toObjectId": "$accountId"}}},
            {
                "$match": {
                    "$expr": {
                        "$and": [
                            {"$eq": ["$accountObjectId", "$$accountId"]},
                            { "$eq": ["$isDraft", False] },
                        ]
                    }
                }
            },
        ],
        "as": "transactions",
    }
}

ACCOUNTS_AGGREGATE_QUERY = {
    "$addFields": {
        "totalCredit": {
            "$sum": {
                "$map": {
                    "input": {
                        "$filter": {
                            "input": "$transactions",
                            "as": "txn",
                            "cond": {"$eq": ["$$txn.transactionType", "CREDIT"]},
                        }
                    },
                    "as": "creditTxn",
                    "in": "$$creditTxn.amount",
                }
            }
        },
        "totalDebit": {
            "$sum": {
                "$map": {
                    "input": {
                        "$filter": {
                            "input": "$transactions",
                            "as": "txn",
                            "cond": {"$eq": ["$$txn.transactionType", "DEBIT"]},
                        }
                    },
                    "as": "debitTxn",
                    "in": "$$debitTxn.amount",
                }
            }
        },
    }
}

ACCOUNTS_ADD_FIELDS_QUERY = {
    "$addFields": {
        "currentBalance": {
            "$add": [
                {"$toDouble": "$amount"},
                {"$subtract": ["$totalCredit", "$totalDebit"]},
            ]
        }
    }
}

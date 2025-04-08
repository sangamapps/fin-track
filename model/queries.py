def getAccountAggregateQuery(userId, isDraft=0, accountId=None):
    match_stage = {"userId": userId}
    if accountId:
        match_stage["_id"] = accountId
    return [
        {"$match": match_stage},
        {
            "$lookup": {
                "from": "transactions",
                "let": {"accId": "$_id", "userId": "$userId"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$accountId", "$$accId"]},
                                    {"$eq": ["$userId", "$$userId"]},
                                    {"$eq": ["$isDraft", isDraft]},
                                ]
                            }
                        }
                    },
                    {
                        "$group": {
                            "_id": None,
                            "totalCredit": {
                                "$sum": {
                                    "$cond": [
                                        {"$eq": ["$type", "CREDIT"]},
                                        "$amount",
                                        0,
                                    ]
                                }
                            },
                            "totalDebit": {
                                "$sum": {
                                    "$cond": [{"$eq": ["$type", "DEBIT"]}, "$amount", 0]
                                }
                            },
                        }
                    },
                ],
                "as": "transactionSummary",
            }
        },
        {
            "$unwind": {
                "path": "$transactionSummary",
                "preserveNullAndEmptyArrays": True,
            }
        },
        {
            "$addFields": {
                "totalCredit": {"$ifNull": ["$transactionSummary.totalCredit", 0]},
                "totalDebit": {"$ifNull": ["$transactionSummary.totalDebit", 0]},
                "closingBalance": {
                    "$subtract": [
                        {
                            "$add": [
                                "$openingBalance",
                                {"$ifNull": ["$transactionSummary.totalCredit", 0]},
                            ]
                        },
                        {"$ifNull": ["$transactionSummary.totalDebit", 0]},
                    ]
                },
            }
        },
        {"$project": {"transactionSummary": 0}},
    ]

class Transaction:
    KEY_ID = "_id"
    KEY_USER_ID = "userId"
    KEY_DATE = "date"
    KEY_IS_DRAFT = "isDraft"
    KEY_ACCOUNT_ID = "accountId"
    KEY_DESCRIPTION = "description"
    KEY_TRANSACTION_TYPE = "transactionType"
    KEY_AMOUNT = "amount"
    KEY_APPLIED_RULES = "appliedRules"
    KEY_COMMENTS = "comments"
    KEY_CREATED_AT = "createdAt"
    KEY_UPDATED_AT = "updatedAt"

    def __init__(self, record: dict):
        self._id = record.get(self.KEY_ID, "")
        self.userId = record.get(self.KEY_USER_ID, "")
        self.date = record.get(self.KEY_DATE, "")
        self.isDraft = record.get(self.KEY_IS_DRAFT, False)
        self.accountId = record.get(self.KEY_ACCOUNT_ID, "")
        self.description = record.get(self.KEY_DESCRIPTION, "")
        self.transactionType = record.get(self.KEY_TRANSACTION_TYPE, "")
        self.amount = record.get(self.KEY_AMOUNT, 0)
        self.appliedRules = record.get(self.KEY_APPLIED_RULES, {})
        self.comments = record.get(self.KEY_COMMENTS, "")
        self.createdAt = record.get(self.KEY_CREATED_AT, "")
        self.updatedAt = record.get(self.KEY_UPDATED_AT, "")

    def json(self) -> dict:
        return {
            self.KEY_ID: self._id,
            self.KEY_USER_ID: self.userId,
            self.KEY_DATE: self.date,
            self.KEY_IS_DRAFT: self.isDraft,
            self.KEY_ACCOUNT_ID: self.accountId,
            self.KEY_DESCRIPTION: self.description,
            self.KEY_TRANSACTION_TYPE: self.transactionType,
            self.KEY_AMOUNT: self.amount,
            self.KEY_APPLIED_RULES: self.appliedRules,
            self.KEY_COMMENTS: self.comments,
            self.KEY_CREATED_AT: self.createdAt,
            self.KEY_UPDATED_AT: self.updatedAt,
        }

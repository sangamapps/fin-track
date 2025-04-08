from bson import ObjectId
from datetime import datetime, timezone


class Transaction:
    KEY_ID = "_id"
    KEY_USER_ID = "userId"
    KEY_DATE = "date"
    KEY_IS_DRAFT = "isDraft"
    KEY_ACCOUNT_ID = "accountId"
    KEY_DESCRIPTION = "description"
    KEY_TYPE = "type"
    KEY_AMOUNT = "amount"
    KEY_BALANCE = "balance"
    KEY_APPLIED_RULES = "appliedRules"
    KEY_COMMENTS = "comments"
    KEY_CREATED_AT = "createdAt"
    KEY_UPDATED_AT = "updatedAt"

    def __init__(self, record: dict):
        self._id = record.get(self.KEY_ID)
        self.userId = record.get(self.KEY_USER_ID)
        self.date = record.get(self.KEY_DATE)
        self.isDraft = record.get(self.KEY_IS_DRAFT)
        self.accountId = record.get(self.KEY_ACCOUNT_ID)
        self.description = record.get(self.KEY_DESCRIPTION)
        self.type = record.get(self.KEY_TYPE)
        self.amount = record.get(self.KEY_AMOUNT)
        self.balance = record.get(self.KEY_BALANCE, 0)
        self.appliedRules = record.get(self.KEY_APPLIED_RULES)
        self.comments = record.get(self.KEY_COMMENTS)
        self.createdAt = record.get(self.KEY_CREATED_AT)
        self.updatedAt = record.get(self.KEY_UPDATED_AT)

    def validate(self):
        # validate userId
        if not isinstance(self.userId, str):
            raise Exception("userId must be a string")
        if self.userId == "":
            raise Exception("userId is required")
        try:
            self.userId = ObjectId(self.userId)
        except Exception:
            raise Exception("userId is not a valid ObjectId")

        # validate date
        if not isinstance(self.date, str):
            raise Exception("date must be a string")
        if self.date == "":
            raise Exception("date is required")

        # validate isDraft
        if not isinstance(self.isDraft, int):
            raise Exception("isDraft must be a number")

        # validate accountId
        if not isinstance(self.accountId, str):
            raise Exception("accountId must be a string")
        if self.accountId == "":
            raise Exception("accountId is required")
        try:
            self.accountId = ObjectId(self.accountId)
        except Exception:
            raise Exception("accountId is not a valid ObjectId")

        # validate description
        if not isinstance(self.description, str):
            raise Exception("description must be a string")

        # validate type
        if not isinstance(self.type, str):
            raise Exception("type must be a string")
        if self.type == "":
            raise Exception("type is required")

        # validate amount
        if not isinstance(self.amount, int) and not isinstance(self.amount, float):
            raise Exception("amount must be a number")
        if self.amount == 0:
            raise Exception("amount is required")

        # validate balance
        if not isinstance(self.balance, int) and not isinstance(self.balance, float):
            raise Exception("balance must be a number")

        # validate appliedRules
        if not isinstance(self.appliedRules, dict):
            raise Exception("appliedRules must be a dictionary")

        # validate comments
        if not isinstance(self.comments, str):
            raise Exception("comments must be a string")

    def json(self) -> dict:
        return {
            self.KEY_USER_ID: self.userId,
            self.KEY_DATE: self.date,
            self.KEY_IS_DRAFT: self.isDraft,
            self.KEY_ACCOUNT_ID: self.accountId,
            self.KEY_DESCRIPTION: self.description,
            self.KEY_TYPE: self.type,
            self.KEY_AMOUNT: self.amount,
            self.KEY_BALANCE: self.balance,
            self.KEY_APPLIED_RULES: self.appliedRules,
            self.KEY_COMMENTS: self.comments,
        }

    def jsonResponse(self) -> dict:
        return {
            self.KEY_ID: str(self._id),
            self.KEY_USER_ID: str(self.userId),
            self.KEY_DATE: self.date,
            self.KEY_IS_DRAFT: self.isDraft,
            self.KEY_ACCOUNT_ID: str(self.accountId),
            self.KEY_DESCRIPTION: self.description,
            self.KEY_TYPE: self.type,
            self.KEY_AMOUNT: self.amount,
            self.KEY_BALANCE: self.balance,
            self.KEY_APPLIED_RULES: self.appliedRules,
            self.KEY_COMMENTS: self.comments,
            self.KEY_CREATED_AT: self.createdAt,
            self.KEY_UPDATED_AT: self.updatedAt,
        }


class CreateTransaction(Transaction):
    def __init__(self, record: dict):
        super().__init__(record)
        self.createdAt = datetime.now(timezone.utc)
        self.updatedAt = datetime.now(timezone.utc)

        super().validate()

    def json(self) -> dict:
        return {
            **super().json(),
            self.KEY_CREATED_AT: self.createdAt,
            self.KEY_UPDATED_AT: self.updatedAt,
        }


class UpdateTransaction(Transaction):
    def __init__(self, record: dict):
        super().__init__(record)
        self.updatedAt = datetime.now(timezone.utc)

        self.validate()

    def validate(self):
        # validate _id
        if not isinstance(self._id, str):
            raise Exception("_id must be a string")
        if self._id == "":
            raise Exception("_id is required")
        try:
            self._id = ObjectId(self._id)
        except Exception:
            raise Exception("_id is not a valid ObjectId")

        # validate super
        super().validate()

    def json(self) -> dict:
        return {
            **super().json(),
            self.KEY_UPDATED_AT: self.updatedAt,
        }

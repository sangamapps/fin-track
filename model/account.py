from bson import ObjectId
from datetime import datetime, timezone


class Account:
    KEY_ID = "_id"
    KEY_USER_ID = "userId"
    KEY_TYPE = "type"
    KEY_NAME = "name"
    KEY_OPENING_BALANCE = "openingBalance"
    KEY_TOTAL_DEBIT = "totalDebit"
    KEY_TOTAL_CREDIT = "totalCredit"
    KEY_CLOSING_BALANCE = "closingBalance"
    KEY_DESCRIPTION = "description"
    KEY_CREATED_AT = "createdAt"
    KEY_UPDATED_AT = "updatedAt"

    def __init__(self, record: dict):
        self._id = record.get(Account.KEY_ID)
        self.userId = record.get(Account.KEY_USER_ID)
        self.type = record.get(Account.KEY_TYPE)
        self.name = record.get(Account.KEY_NAME)
        self.openingBalance = record.get(Account.KEY_OPENING_BALANCE)
        self.totalDebit = record.get(Account.KEY_TOTAL_DEBIT)
        self.totalCredit = record.get(Account.KEY_TOTAL_CREDIT)
        self.closingBalance = record.get(Account.KEY_CLOSING_BALANCE)
        self.description = record.get(Account.KEY_DESCRIPTION)
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

        # validate type
        if not isinstance(self.type, str):
            raise Exception("type must be a string")
        if self.type == "":
            raise Exception("type is required")

        # validate name
        if not isinstance(self.name, str):
            raise Exception("name must be a string")
        if self.name == "":
            raise Exception("name is required")

        # validate openingBalance
        if not isinstance(self.openingBalance, int) and not isinstance(self.openingBalance, float):
            raise Exception("openingBalance must be a number")

        # validate description
        if not isinstance(self.description, str):
            raise Exception("description must be a string")

    def json(self) -> dict:
        return {
            Account.KEY_USER_ID: self.userId,
            Account.KEY_TYPE: self.type,
            Account.KEY_NAME: self.name,
            Account.KEY_OPENING_BALANCE: self.openingBalance,
            Account.KEY_DESCRIPTION: self.description,
        }
    
    def jsonResponse(self) -> dict:
        return {
            Account.KEY_ID: str(self._id),
            Account.KEY_USER_ID: str(self.userId),
            Account.KEY_TYPE: self.type,
            Account.KEY_NAME: self.name,
            Account.KEY_OPENING_BALANCE: self.openingBalance,
            Account.KEY_TOTAL_DEBIT: self.totalDebit,
            Account.KEY_TOTAL_CREDIT: self.totalCredit,
            Account.KEY_CLOSING_BALANCE: self.closingBalance,
            Account.KEY_DESCRIPTION: self.description,
        }


class CreateAccount(Account):
    def __init__(self, record: dict):
        super().__init__(record)
        self.totalCredit = 0
        self.totalDebit = 0
        self.closingBalance = self.openingBalance
        self.createdAt = datetime.now(timezone.utc)
        self.updatedAt = datetime.now(timezone.utc)

        super().validate()

    def json(self) -> dict:
        return {
            **super().json(),
            Account.KEY_CREATED_AT: self.createdAt,
            Account.KEY_UPDATED_AT: self.updatedAt,
        }


class UpdateAccount(Account):
    def __init__(self, record: dict):
        super().__init__(record)
        self._id = record.get(Account.KEY_ID)
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
            Account.KEY_UPDATED_AT: self.updatedAt,
        }

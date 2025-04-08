from bson import ObjectId
from datetime import datetime, timezone


class Rule:
    KEY_ID = "_id"
    KEY_USER_ID = "userId"
    KEY_TAG = "tag"
    KEY_KEYWORDS = "keywords"
    KEY_DESCRIPTION = "description"
    KEY_CREATED_AT = "createdAt"
    KEY_UPDATED_AT = "updatedAt"

    def __init__(self, record: dict):
        self._id = record.get(self.KEY_ID)
        self.userId = record.get(self.KEY_USER_ID)
        self.tag = record.get(self.KEY_TAG)
        self.keywords = record.get(self.KEY_KEYWORDS)
        self.description = record.get(self.KEY_DESCRIPTION)
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

        # validate tag
        if not isinstance(self.tag, str):
            raise Exception("tag must be a string")

        # validate keywords
        if not isinstance(self.keywords, str):
            raise Exception("keywords must be a list")
        if self.keywords == "":
            raise Exception("keywords is required")

        # validate description
        if not isinstance(self.description, str):
            raise Exception("description must be a string")

    def json(self) -> dict:
        return {
            self.KEY_USER_ID: self.userId,
            self.KEY_TAG: self.tag,
            self.KEY_KEYWORDS: self.keywords,
            self.KEY_DESCRIPTION: self.description,
        }

    def jsonResponse(self) -> dict:
        return {
            self.KEY_ID: str(self._id),
            self.KEY_USER_ID: str(self.userId),
            self.KEY_TAG: self.tag,
            self.KEY_KEYWORDS: self.keywords,
            self.KEY_DESCRIPTION: self.description,
            self.KEY_CREATED_AT: self.createdAt,
            self.KEY_UPDATED_AT: self.updatedAt,
        }

class CreateRule(Rule):
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


class UpdateRule(Rule):
    def __init__(self, record: dict):
        super().__init__(record)
        self._id = record.get(self.KEY_ID)
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

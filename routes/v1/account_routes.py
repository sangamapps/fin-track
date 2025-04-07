from flask import Blueprint, request, session
from model.mongodb import accounts_collection, ObjectId
from model.queries import ACCOUNTS_LOOKUP_QUERY, ACCOUNTS_AGGREGATE_QUERY, ACCOUNTS_ADD_FIELDS_QUERY

account_routes_bp = Blueprint("account_routes", __name__)


@account_routes_bp.route("/accounts", methods=["GET"])
def get_accounts():
    userId = session["user"]["_id"]
    query_pipeline = [
        {"$match": {"userId": userId}},
        ACCOUNTS_LOOKUP_QUERY,
        ACCOUNTS_AGGREGATE_QUERY,
        ACCOUNTS_ADD_FIELDS_QUERY,
        {"$project":{"transactions":0}}
    ]
    accounts = list(accounts_collection.aggregate(query_pipeline))
    for account in accounts:
        account["_id"] = str(account["_id"])
    return {"accounts": accounts}


@account_routes_bp.route("/account", methods=["POST"])
def upsert_account():
    userId = session["user"]["_id"]
    data = request.get_json()
    _id = data.pop("_id", None)
    if _id:
        query = {"userId":userId, "_id": ObjectId(_id)}
        result = accounts_collection.update_one(query, {"$set": data})
        data["_id"] = _id
    else:
        data["userId"] = userId
        result = accounts_collection.insert_one(data)
        data["_id"] = str(result.inserted_id)
    return {"account": data}


@account_routes_bp.route("/account/<_id>", methods=["DELETE"])
def delete_account(_id):
    userId = session["user"]["_id"]
    result = accounts_collection.delete_one({"userId":userId, "_id": ObjectId(_id)})
    if result.deleted_count == 0:
        return {"message": "Account not found"}, 404
    return {"_id": _id}

from flask import Blueprint, request
from model.mongodb import accounts_collection, ObjectId

account_routes_bp = Blueprint("account_routes", __name__)


@account_routes_bp.route("/accounts", methods=["GET"])
def get_accounts():
    accounts = list(accounts_collection.find({}))
    for account in accounts:
        account["_id"] = str(account["_id"])
    return {"accounts": accounts}


@account_routes_bp.route("/account", methods=["POST"])
def upsert_account():
    data = request.get_json()
    _id = data.pop("_id", None)
    if _id:
        query = {"_id": ObjectId(_id)}
        result = accounts_collection.update_one(query, {"$set": data})
        data["_id"] = _id
    else:
        result = accounts_collection.insert_one(data)
        data["_id"] = str(result.inserted_id)
    return data


@account_routes_bp.route("/account/<_id>", methods=["DELETE"])
def delete_account(_id):
    result = accounts_collection.delete_one({"_id": ObjectId(_id)})
    if result.deleted_count == 0:
        return {"error": "Account not found"}, 404
    return {"message": "Account deleted"}

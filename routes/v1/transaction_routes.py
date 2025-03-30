from flask import Blueprint, request
from model.mongodb import transactions_collection, ObjectId
from datetime import datetime, timezone
import extractor as Extractor

transaction_routes_bp = Blueprint('extractor', __name__)

@transaction_routes_bp.route("/transactions/extract", methods=["POST"])
def extract_transactions():
    extractor = request.form["extractor"]
    file = request.files["file"]
    transactions = Extractor.extract(extractor, file)
    processed_transactions = Extractor.rename_columns(transactions)
    return {
        "processed_transactions": processed_transactions,
    }

@transaction_routes_bp.route("/transactions/save", methods=["POST"])
def save_transactions():
    account = request.json["account"]
    transactions = request.json["transactions"]
    for transaction in transactions:
        transaction["account"] = account
        transaction["createdAt"] = datetime.now(timezone.utc)
        transaction["updatedAt"] = datetime.now(timezone.utc)
    transactions_collection.insert_many(transactions)
    return {"success": True}

@transaction_routes_bp.route("/transactions", methods=["GET"])
def get_transactions():
    transactions = list(transactions_collection.find({}))
    for transaction in transactions:
        transaction["_id"] = str(transaction["_id"])
    return {"transactions": transactions}

@transaction_routes_bp.route("/transaction", methods=["POST"])
def upsert_transaction():
    data = request.get_json()
    _id = data.pop("_id", None)
    if _id:
        query = {"_id": ObjectId(_id)}
        result = transactions_collection.update_one(query, {"$set": data})
        data["_id"] = _id
    else:
        result = transactions_collection.insert_one(data)
        data["_id"] = str(result.inserted_id)
    return data


@transaction_routes_bp.route("/transaction/<_id>", methods=["DELETE"])
def delete_transaction(_id):
    result = transactions_collection.delete_one({"_id": ObjectId(_id)})
    if result.deleted_count == 0:
        return {"error": "transaction not found"}, 404
    return {"message": "transaction deleted"}
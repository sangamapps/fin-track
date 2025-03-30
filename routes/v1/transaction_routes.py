from flask import Blueprint, request
from model.mongodb import transactions_collection, ObjectId
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
    transactions = request.json["transactions"]
    transactions_collection.insert_many(transactions)
    return {"success": True}

@transaction_routes_bp.route("/transactions", methods=["GET"])
def get_transactions():
    transactions = list(transactions_collection.find({}))
    for transaction in transactions:
        transaction["_id"] = str(transaction["_id"])
    return {"transactions": transactions}
from flask import Blueprint, request
from model.mongodb import transactions_collection, ObjectId
from model.transaction import Transaction
from datetime import datetime, timezone
import extractor as Extractor

transaction_routes_bp = Blueprint('extractor', __name__)

@transaction_routes_bp.route("/transactions/extract", methods=["POST"])
def extract_transactions():
    extractor = request.form["extractor"]
    file = request.files["file"]
    transactions = Extractor.extract(extractor, file)
    processed_transactions = [Transaction(transaction).json() for transaction in Extractor.rename_columns(transactions)]
    return {
        "processed_transactions": processed_transactions,
    }

@transaction_routes_bp.route("/transactions/save", methods=["POST"])
def save_transactions():
    account = request.json["account"]
    transactions = []
    for transaction in request.json["transactions"]:
        mTransaction = Transaction(transaction)
        mTransaction.account = account
        mTransaction.createdAt = datetime.now(timezone.utc)
        mTransaction.updatedAt = datetime.now(timezone.utc)
        transaction = mTransaction.json()
        transaction.pop(Transaction.KEY_ID)
        transactions.append(transaction)
    transactions_collection.insert_many(transactions)
    return {"success": True}

@transaction_routes_bp.route("/transactions", methods=["GET"])
def get_transactions():
    transactions = list(transactions_collection.find({}))
    mTransactions = []
    for transaction in transactions:
        mTransaction = Transaction(transaction)
        mTransaction._id = str(mTransaction._id)
        transaction = mTransaction.json()
        mTransactions.append(mTransaction.json())
    return {"transactions": mTransactions}

@transaction_routes_bp.route("/transaction", methods=["POST"])
def upsert_transaction():
    data = request.get_json()
    mTransaction = Transaction(data)
    mTransaction.updatedAt = datetime.now(timezone.utc)
    transaction = mTransaction.json()
    _id = transaction.pop(Transaction.KEY_ID)
    if _id != "":
        query = {Transaction.KEY_ID: ObjectId(_id)}
        result = transactions_collection.update_one(query, {"$set": transaction})
        transaction[Transaction.KEY_ID] = _id
    else:
        transaction[Transaction.KEY_CREATED_AT] = datetime.now(timezone.utc)
        result = transactions_collection.insert_one(transaction)
        transaction[Transaction.KEY_ID] = str(result.inserted_id)
    return transaction


@transaction_routes_bp.route("/transaction/<_id>", methods=["DELETE"])
def delete_transaction(_id):
    result = transactions_collection.delete_one({Transaction.KEY_ID: ObjectId(_id)})
    if result.deleted_count == 0:
        return {"error": "transaction not found"}, 404
    return {"message": "transaction deleted"}
from flask import Blueprint, request, session
from model.mongodb import transactions_collection, ObjectId
from model.transaction import Transaction
from datetime import datetime, timezone
import extractor as Extractor

transaction_routes_bp = Blueprint('extractor', __name__)

@transaction_routes_bp.route("/transactions/extract", methods=["POST"])
def extract_transactions():
    userId = session["user"]["_id"]
    accountId = request.form[Transaction.KEY_ACCOUNT_ID]
    transactions = []
    for transaction in Extractor.extract(request.form["extractor"], request.files["file"]):
        mTransaction = Transaction(transaction)
        mTransaction.userId = userId
        mTransaction.accountId = accountId
        mTransaction.isDraft = True
        mTransaction.createdAt = datetime.now(timezone.utc)
        mTransaction.updatedAt = datetime.now(timezone.utc)
        transaction = mTransaction.json()
        transaction.pop(Transaction.KEY_ID)
        transactions.append(transaction)
    transactions_collection.insert_many(transactions)
    return {"transactionsCount": len(transactions)}

@transaction_routes_bp.route("/transactions/save", methods=["POST"])
def save_transactions():
    userId = session["user"]["_id"]
    transactions_collection.update_many({Transaction.KEY_USER_ID:userId, Transaction.KEY_IS_DRAFT:True},{"$set":{Transaction.KEY_IS_DRAFT:False}})
    return {"success": True}

@transaction_routes_bp.route("/transactions", methods=["GET"])
def get_transactions():
    userId = session["user"]["_id"]
    startDate = request.args.get("startDate")
    endDate = request.args.get("endDate")
    isDraft = True if request.args.get("isDraft") == "true" else False
    query = {Transaction.KEY_USER_ID:userId, Transaction.KEY_IS_DRAFT: isDraft}
    dateFilter = {}
    if startDate:
        dateFilter["$gte"] = startDate
    if endDate:
        dateFilter["$lte"] = endDate
    if dateFilter:
        query.update({Transaction.KEY_DATE: dateFilter})
    transactions = list(transactions_collection.find(query))
    mTransactions = []
    for transaction in transactions:
        mTransaction = Transaction(transaction)
        mTransaction._id = str(mTransaction._id)
        transaction = mTransaction.json()
        mTransactions.append(mTransaction.json())
    return {"transactions": mTransactions}

@transaction_routes_bp.route("/transaction", methods=["POST"])
def upsert_transaction():
    userId = session["user"]["_id"]
    data = request.get_json()
    mTransaction = Transaction(data)
    mTransaction.updatedAt = datetime.now(timezone.utc)
    transaction = mTransaction.json()
    _id = transaction.pop(Transaction.KEY_ID)
    if _id != "":
        query = {Transaction.KEY_USER_ID:userId, Transaction.KEY_ID: ObjectId(_id)}
        result = transactions_collection.update_one(query, {"$set": transaction})
        transaction[Transaction.KEY_ID] = _id
    else:
        transaction[Transaction.KEY_USER_ID] = userId
        transaction[Transaction.KEY_CREATED_AT] = datetime.now(timezone.utc)
        result = transactions_collection.insert_one(transaction)
        transaction[Transaction.KEY_ID] = str(result.inserted_id)
    return { "transaction": transaction}


@transaction_routes_bp.route("/transaction/<_id>", methods=["DELETE"])
def delete_transaction(_id):
    userId = session["user"]["_id"]
    result = transactions_collection.delete_one({Transaction.KEY_ID: ObjectId(_id)})
    if result.deleted_count == 0:
        return {"success":False,"message": "Transaction not found"}, 404
    return {"success": True, "_id": _id}

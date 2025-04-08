from flask import Blueprint, request, session
from bson import ObjectId
from model.mongodb import transactions_collection
from model.transaction import Transaction, CreateTransaction, UpdateTransaction
import extractor as Extractor

transaction_routes_bp = Blueprint("extractor", __name__)


@transaction_routes_bp.route("/transactions/extract", methods=["POST"])
def extract_transactions():
    userId = session["user"]["_id"]
    accountId = request.form[Transaction.KEY_ACCOUNT_ID]
    extracted_transactions = Extractor.extract(request.form["extractor"], request.files["file"])
    transactions = []
    for extracted_transaction in extracted_transactions:
        extracted_transaction[Transaction.KEY_USER_ID] = userId
        extracted_transaction[Transaction.KEY_ACCOUNT_ID] = accountId
        extracted_transaction[Transaction.KEY_IS_DRAFT] = 1
        create_transaction = CreateTransaction(extracted_transaction)
        transactions.append(create_transaction.json())
    transactions_collection.insert_many(transactions)
    return {"transactionsCount": len(transactions)}


@transaction_routes_bp.route("/transactions/save-drafts", methods=["POST"])
def save_drafts():
    userId = session["user"]["_id"]
    query = {Transaction.KEY_USER_ID: ObjectId(userId), Transaction.KEY_IS_DRAFT: 1}
    transactions_collection.update_many(query, {"$set": {Transaction.KEY_IS_DRAFT: 0}})
    return {"success": True}


@transaction_routes_bp.route("/transactions/delete-drafts", methods=["POST"])
def delete_drafts():
    userId = session["user"]["_id"]
    query = {Transaction.KEY_USER_ID: ObjectId(userId), Transaction.KEY_IS_DRAFT: 1}
    transactions_collection.delete_many(query)
    return {"success": True}


@transaction_routes_bp.route("/transactions", methods=["GET"])
def get_transactions():
    userId = session["user"]["_id"]
    startDate = request.args.get("startDate")
    endDate = request.args.get("endDate")
    sortByDate = int(request.args.get("sortByDate"))
    isDraft = int(request.args.get("isDraft"))
    query = {
        Transaction.KEY_USER_ID: ObjectId(userId),
        Transaction.KEY_IS_DRAFT: isDraft,
    }
    dateFilter = {}
    if startDate:
        dateFilter["$gte"] = startDate
    if endDate:
        dateFilter["$lte"] = endDate
    if dateFilter:
        query.update({Transaction.KEY_DATE: dateFilter})
    sortQuery = {Transaction.KEY_DATE: sortByDate, Transaction.KEY_DATE: 1}
    result = transactions_collection.find(query).sort(sortQuery)
    transactions = [Transaction(transaction).jsonResponse() for transaction in list(result)]
    return {"transactions": transactions}


@transaction_routes_bp.route("/transaction", methods=["POST"])
def upsert_transaction():
    userId = session["user"]["_id"]
    transaction = request.get_json()
    _id = transaction[Transaction.KEY_ID] if Transaction.KEY_ID in transaction else ""
    if _id != "":
        transaction[Transaction.KEY_USER_ID] = userId
        update_transaction = UpdateTransaction(transaction)
        query = {
            Transaction.KEY_USER_ID: update_transaction.userId,
            Transaction.KEY_ID: update_transaction._id,
        }
        result = transactions_collection.update_one(query, {"$set": update_transaction.json()})
        transaction = update_transaction.jsonResponse()
    else:
        transaction[Transaction.KEY_USER_ID] = userId
        create_transaction = CreateTransaction(transaction)
        result = transactions_collection.insert_one(create_transaction.json())
        create_transaction._id = result.inserted_id
        transaction = create_transaction.jsonResponse()
    return {"transaction": transaction}


@transaction_routes_bp.route("/transaction/<_id>", methods=["DELETE"])
def delete_transaction(_id):
    userId = session["user"]["_id"]
    query = {
        Transaction.KEY_USER_ID: ObjectId(userId),
        Transaction.KEY_ID: ObjectId(_id),
    }
    result = transactions_collection.delete_one(query)
    if result.deleted_count == 0:
        return {"success": False, "message": "Transaction not found"}, 404
    return {"success": True, Transaction.KEY_ID: _id}

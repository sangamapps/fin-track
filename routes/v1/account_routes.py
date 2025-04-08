from flask import Blueprint, request, session
from bson import ObjectId
from model.mongodb import accounts_collection
from model.account import Account, CreateAccount, UpdateAccount
from model.queries import getAccountAggregateQuery

account_routes_bp = Blueprint("account_routes", __name__)


@account_routes_bp.route("/accounts", methods=["GET"])
def get_accounts():
    userId = session["user"]["_id"]
    query_pipeline = getAccountAggregateQuery(userId=ObjectId(userId))
    result = accounts_collection.aggregate(query_pipeline)
    accounts = [Account(account).jsonResponse() for account in list(result)]
    return {"accounts": accounts}


@account_routes_bp.route("/account", methods=["POST"])
def upsert_account():
    userId = session["user"]["_id"]
    account = request.get_json()
    _id = account[Account.KEY_ID] if Account.KEY_ID in account else ""
    if _id != "":
        account[Account.KEY_USER_ID] = userId
        update_account = UpdateAccount(account)
        query = {Account.KEY_USER_ID: update_account.userId, Account.KEY_ID: update_account._id}
        result = accounts_collection.update_one(query, {"$set": update_account.json()})
        result = accounts_collection.aggregate(getAccountAggregateQuery(userId=update_account.userId,accountId=update_account._id))
        account = Account(list(result)[0]).jsonResponse()
    else:
        account[Account.KEY_USER_ID] = userId
        create_account = CreateAccount(account)
        result = accounts_collection.insert_one(create_account.json())
        create_account._id = result.inserted_id
        account = create_account.jsonResponse()
    return {"account": account}


@account_routes_bp.route("/account/<_id>", methods=["DELETE"])
def delete_account(_id):
    userId = session["user"]["_id"]
    query = {Account.KEY_USER_ID: ObjectId(userId), Account.KEY_ID: ObjectId(_id)}
    result = accounts_collection.delete_one(query)
    if result.deleted_count == 0:
        return {"message": "Account not found"}, 404
    return {Account.KEY_ID: _id}

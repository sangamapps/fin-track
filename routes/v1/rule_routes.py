from flask import Blueprint, request, session
from model.mongodb import rules_collection, ObjectId

rule_routes_bp = Blueprint("rule_routes", __name__)


@rule_routes_bp.route("/rules", methods=["GET"])
def get_rules():
    userId = session["user"]["_id"]
    rules = list(rules_collection.find({"userId":userId}))
    for rule in rules:
        rule["_id"] = str(rule["_id"])
    return {"rules": rules}


@rule_routes_bp.route("/rule", methods=["POST"])
def upsert_rule():
    userId = session["user"]["_id"]
    data = request.get_json()
    _id = data.pop("_id", None)
    if _id:
        query = {"userId":userId, "_id": ObjectId(_id)}
        result = rules_collection.update_one(query, {"$set": data})
        data["_id"] = _id
    else:
        data["userId"] = userId
        result = rules_collection.insert_one(data)
        data["_id"] = str(result.inserted_id)
    return {"rule": data}


@rule_routes_bp.route("/rule/<_id>", methods=["DELETE"])
def delete_rule(_id):
    userId = session["user"]["_id"]
    result = rules_collection.delete_one({"userId":userId, "_id": ObjectId(_id)})
    if result.deleted_count == 0:
        return {"message": "Rule not found"}, 404
    return {"_id": _id}

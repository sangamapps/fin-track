from flask import Blueprint, request
from model.mongodb import rules_collection, ObjectId

rule_routes_bp = Blueprint("rule_routes", __name__)


@rule_routes_bp.route("/rules", methods=["GET"])
def get_rules():
    rules = list(rules_collection.find({}))
    for rule in rules:
        rule["_id"] = str(rule["_id"])
    return {"rules": rules}


@rule_routes_bp.route("/rule", methods=["POST"])
def upsert_rule():
    data = request.get_json()
    _id = data.pop("_id", None)
    if _id:
        query = {"_id": ObjectId(_id)}
        result = rules_collection.update_one(query, {"$set": data})
        data["_id"] = _id
    else:
        result = rules_collection.insert_one(data)
        data["_id"] = str(result.inserted_id)
    return data


@rule_routes_bp.route("/rule/<_id>", methods=["DELETE"])
def delete_rule(_id):
    result = rules_collection.delete_one({"_id": ObjectId(_id)})
    if result.deleted_count == 0:
        return {"error": "Account not found"}, 404
    return {"message": "Account deleted"}

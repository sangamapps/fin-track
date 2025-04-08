from flask import Blueprint, request, session
from bson import ObjectId
from model.mongodb import rules_collection
from model.rule import Rule, CreateRule, UpdateRule

rule_routes_bp = Blueprint("rule_routes", __name__)


@rule_routes_bp.route("/rules", methods=["GET"])
def get_rules():
    userId = session["user"]["_id"]
    result = rules_collection.find({Rule.KEY_USER_ID:ObjectId(userId)})
    rules = [Rule(rule).jsonResponse() for rule in list(result)]
    return {"rules": rules}


@rule_routes_bp.route("/rule", methods=["POST"])
def upsert_rule():
    userId = session["user"]["_id"]
    rule = request.get_json()
    _id = rule[Rule.KEY_ID] if Rule.KEY_ID in rule else ""
    if _id != "":
        rule[Rule.KEY_USER_ID] = userId
        update_rule = UpdateRule(rule)
        query = {Rule.KEY_USER_ID:update_rule.userId, Rule.KEY_ID: update_rule._id}
        result = rules_collection.update_one(query, {"$set": update_rule.json()})
        rule = update_rule.jsonResponse()
    else:
        rule[Rule.KEY_USER_ID] = userId
        create_rule = CreateRule(rule)
        result = rules_collection.insert_one(create_rule.json())
        create_rule._id = result.inserted_id
        rule = create_rule.jsonResponse()
    return {"rule": rule}


@rule_routes_bp.route("/rule/<_id>", methods=["DELETE"])
def delete_rule(_id):
    userId = session["user"]["_id"]
    result = rules_collection.delete_one({Rule.KEY_USER_ID:ObjectId(userId), Rule.KEY_ID: ObjectId(_id)})
    if result.deleted_count == 0:
        return {"message": "Rule not found"}, 404
    return {"_id": _id}

from flask import Blueprint, request, session
from google.oauth2 import id_token
from google.auth.transport import requests
from model.mongodb import users_collection, ObjectId
from datetime import datetime, timezone

user_routes_bp = Blueprint('user_routes', __name__)

GOOGLE_CLIENT_ID = "681626859343-dtkml0ds42u48qg1q5nr07kevma99tfk.apps.googleusercontent.com"

def verify_google_token(token):
    try:
        payload = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        return payload
    except ValueError:
        return None

@user_routes_bp.route('/user/login', methods=['POST'])
def login():
    data = request.json
    token = data.get('token')

    if not token:
        return {"message": "Token is missing"}, 400

    user_data = verify_google_token(token)
    print(user_data)

    if not user_data:
        return {"message": "Invalid Token"}, 401
    
    user_email = user_data.get("email")
    
    userSession = {
        "name": user_data.get("name"),
        "email": user_email,
        "picture": user_data.get("picture"),
    }

    user = users_collection.find_one({"email": user_email})
    if not user:
        new_record = {
            "email": user_email,
            "family": {},
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "updatedAt": datetime.now(timezone.utc).isoformat(),
        }
        userId = users_collection.insert_one(new_record).inserted_id
        userSession = userSession | new_record
        userSession["_id"] = str(userId)
    else:
        userSession = userSession | user
        userSession["_id"] = str(userSession["_id"])

    session["user"] = userSession

    return { "user": userSession}

@user_routes_bp.route('/user/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return {"success": True}
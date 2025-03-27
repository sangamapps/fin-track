from flask import Blueprint, request, session
from google.oauth2 import id_token
from google.auth.transport import requests

user_bp = Blueprint('auth', __name__)

GOOGLE_CLIENT_ID = "681626859343-dtkml0ds42u48qg1q5nr07kevma99tfk.apps.googleusercontent.com"

def verify_google_token(token):
    try:
        payload = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        return payload
    except ValueError:
        return None

@user_bp.route('/user/login', methods=['POST'])
def login():
    data = request.json
    token = data.get('token')

    if not token:
        return {"error": "Token is missing"}, 400

    user_data = verify_google_token(token)
    print(user_data)

    if not user_data:
        return {"error": "Invalid Token"}, 401
    
    session['user'] = {
        "name": user_data.get("name"),
        "email": user_data.get("email"),
        "picture": user_data.get("picture"),
    }

    return {
        "success": True,
        "user": session['user']
    }

@user_bp.route('/user/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return {"success": True, "message": "Logged out successfully"}
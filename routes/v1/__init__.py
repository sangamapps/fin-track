from flask import Blueprint
from .account_routes import account_routes_bp
from .rule_routes import rule_routes_bp
from .transaction_routes import transaction_routes_bp
from .user_routes import user_routes_bp

v1_routes_bp = Blueprint('v1_routes', __name__, url_prefix='/api/v1')

v1_routes_bp.register_blueprint(account_routes_bp)
v1_routes_bp.register_blueprint(rule_routes_bp)
v1_routes_bp.register_blueprint(transaction_routes_bp)
v1_routes_bp.register_blueprint(user_routes_bp)
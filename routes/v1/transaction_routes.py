from flask import Blueprint, request
import extractor as Extractor

transaction_routes_bp = Blueprint('extractor', __name__)

@transaction_routes_bp.route("/transactions/extract", methods=["POST"])
def extract_transactions():
    extractor = request.form["extractor"]
    file = request.files["file"]
    transactions = Extractor.extract(extractor, file)
    processed_transactions = Extractor.rename_columns(transactions)
    return {
        "processed_transactions": processed_transactions,
    }
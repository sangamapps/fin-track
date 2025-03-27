from flask import Blueprint, request
import extractor as Extractor

extractor_bp = Blueprint('extractor', __name__)

@extractor_bp.route("/api/v1/extract-transactions", methods=["POST"])
def extract_transactions():
    extractor = request.form["extractor"]
    file = request.files["file"]
    transactions = Extractor.extract(extractor, file)
    processed_transactions = Extractor.rename_columns(transactions)
    return {
        "transactions": transactions,
        "processed_transactions": processed_transactions,
    }
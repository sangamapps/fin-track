from flask import Flask, render_template, send_from_directory, request, redirect
from os import environ
import extractor as Extractor

app = Flask(__name__)


@app.route("/assets/<path:filename>")
def serve_static(filename):
    if int(environ.get("DEBUG", 0)) == 0:
        return redirect("https://sangamapps.github.io/fin-track-cdn/assets/" + filename)
    return send_from_directory("fin-track-ui/assets/", filename)


@app.route("/")
@app.route("/upload")
def home():
    return render_template("index.html")


@app.route("/api/v1/extract-transactions", methods=["POST"])
def extract_transactions():
    extractor = request.form["extractor"]
    file = request.files["file"]
    transactions = Extractor.extract(extractor, file)
    processed_transactions = Extractor.rename_columns(transactions)
    return {
        "transactions": transactions,
        "processed_transactions": processed_transactions,
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(environ.get("PORT", 8080)), debug=int(environ.get("DEBUG", 0)))

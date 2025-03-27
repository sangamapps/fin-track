from flask import Flask, render_template, send_from_directory, session, redirect
from flask_session import Session
from os import environ
from routes.user import user_bp
from routes.extractor import extractor_bp
from json import dumps

app = Flask(__name__)

app.config["SECRET_KEY"] = "FIN_TRACK_APP"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.register_blueprint(user_bp)
app.register_blueprint(extractor_bp)


@app.route("/assets/<path:filename>")
def serve_static(filename):
    if int(environ.get("DEBUG", 0)) == 0:
        return redirect("https://sangamapps.github.io/fin-track-cdn/assets/" + filename)
    return send_from_directory("fin-track-ui/assets/", filename)


@app.route("/")
@app.route("/transactions")
@app.route("/accounts")
@app.route("/rules")
@app.route("/profile")
def home():
    userInfo = session["user"] if 'user' in session else {}
    return render_template("index.html", userInfo=dumps(userInfo))


if __name__ == "__main__":
    host = "0.0.0.0"
    port=int(environ.get("PORT", 8080))
    debug=int(environ.get("DEBUG", 0))
    app.run(host=host, port=port, debug=debug)

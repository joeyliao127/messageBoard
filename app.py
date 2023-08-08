from flask import *

app = Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/member")
def member():
    return render_template("member.html")

app.run(port=3000, debug=True, use_reloader=True)

from flask import Flask, render_template
from auth import auth_bp
from reservations import res_bp

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(res_bp)
# Landing page (Home)
@app.route("/")
def index():
    # For now, we’ll just pass empty rooms until DB is ready
    return render_template("landing.html", rooms=[])

# ------------------------
# Reservation Page
# ------------------------
@app.route("/reservations")
def reservations():
    return render_template("reservations.html")

# ------------------------
# About us Page
# ------------------------
@app.route("/about")
def about():
    return render_template("about.html")

# ------------------------
# confirm Page
# ------------------------
@app.route("/confirm")
def confirm():
    return render_template("confirm.html")


# ------------------------
# lookup Page
# ------------------------
@app.route("/lookup")
def lookup():
    return render_template("lookup.html")





if __name__ == "__main__":
    app.run(debug=True)

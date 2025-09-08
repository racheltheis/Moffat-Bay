from flask import Flask, render_template
from auth import auth_bp

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Register Blueprints
app.register_blueprint(auth_bp)

# Landing page (Home)
@app.route("/")
def index():
    # For now, we’ll just pass empty rooms until DB is ready
    return render_template("landing.html", rooms=[])

if __name__ == "__main__":
    app.run(debug=True)

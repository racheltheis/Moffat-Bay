from flask import Flask
# If using the code as part of main app
import auth_routes  # your login route

app = Flask(__name__)
app.secret_key = "your_secret_key"  # needed for sessions

# If auth_routes uses a Blueprint, you need to register it
# app.register_blueprint(auth_routes.auth_bp)

if __name__ == "__main__":
    app.run(debug=True)

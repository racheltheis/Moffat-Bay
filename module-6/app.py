#backend logic

from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = "super_secret_key"

# ---- Database Connection ----
def get_db_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",         # your credentials
        password="password", # your credentials
        database="MoffatBay"
    )
    return conn

# ---- Home / Landing Page ----
@app.route("/")
def home():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM Rooms WHERE Status = 'Available'")
    rooms = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("landing.html", rooms=rooms)

# ---- Login Page ----
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM Customers WHERE Email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and bcrypt.checkpw(password.encode("utf-8"), user["Password_Hash"].encode("utf-8")):
            session["user_id"] = user["CustomerID"]
            flash("Login successful!")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password.")
            return redirect(url_for("login"))

    return render_template("register_and_signin.html")

# ---- Register ----
@app.route("/register", methods=["POST"])
def register():
    first = request.form["first_name"]
    last = request.form["last_name"]
    phone = request.form["phone"]
    email = request.form["email"]
    password = request.form["password"]

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Customers (First_Name, Last_Name, Email, Phone, Password_Hash)
            VALUES (%s, %s, %s, %s, %s)
        """, (first, last, email, phone, password_hash))
        conn.commit()
        flash("Account created successfully! Please log in.")
    except mysql.connector.IntegrityError:
        flash("Email already exists.")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("login"))

# ---- Logout ----
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out successfully.")
    return redirect(url_for("login"))
    
#run
if __name__ == "__main__":
    app.run(debug=True)


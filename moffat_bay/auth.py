#   auth.py
#   Handles user registration, login, and logout for both customers and employees.
#   Includes input validation, password hashing (bcrypt), and user-friendly flash messages.

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_conn
import re, bcrypt

auth_bp = Blueprint("auth", __name__)

# ------------------------
# Validation Regex
# ------------------------
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^\+?1?\s*\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$")

# ------------------------
# Register (Customers only)
# ------------------------
@auth_bp.get("/register")
def register_get():
    return render_template("register_and_signin.html", mode="register", email="")

@auth_bp.post("/register")
def register_post():
    email = request.form.get("email", "").strip().lower()
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    phone = request.form.get("phone", "").strip()
    password = request.form.get("password", "")

    # ------------------------
    # Input Validation
    # ------------------------
    if not EMAIL_RE.match(email):
        flash("Please enter a valid email address.", "error")
        return render_template("register_and_signin.html", mode="register", email=email)

    if phone and not PHONE_RE.match(phone):
        flash("Please enter a valid phone number (e.g., 123-456-7890).", "error")
        return render_template("register_and_signin.html", mode="register", email=email)

    if not (len(password) >= 8 and
            re.search(r"[0-9]", password) and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password)):
        flash("Password must be 8+ chars and include upper, lower, and a number.", "error")
        return render_template("register_and_signin.html", mode="register", email=email)

    # ------------------------
    # Password Hashing
    # ------------------------
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        conn = get_conn()
        cur = conn.cursor()

        # Generate new account number like CUST1004
        cur.execute("SELECT MAX(CustomerID) FROM Customers")
        max_id = cur.fetchone()[0] or 0
        account_number = f"CUST{1000 + max_id + 1}"

        # Insert new customer
        cur.execute(
            """INSERT INTO Customers 
               (Account_Number, First_Name, Last_Name, Email, Password_Hash, Phone)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (account_number, first_name, last_name, email, pw_hash, phone)
        )
        conn.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login_get"))

    except Exception as e:
        conn.rollback()
        flash(f"Registration failed: {e}", "error")
        return render_template("register_and_signin.html", mode="register", email=email)

    finally:
        cur.close()
        conn.close()


# ------------------------
# Login (Customers + Employees)
# ------------------------
@auth_bp.get("/login")
def login_get():
    return render_template("register_and_signin.html", mode="login", email="")

@auth_bp.post("/login")
def login_post():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    try:
        conn = get_conn()
        cur = conn.cursor(dictionary=True)

        # Try customer login first
        cur.execute("SELECT * FROM Customers WHERE Email=%s", (email,))
        user = cur.fetchone()
        role = "customer"

        # Try employee if not found
        if not user:
            cur.execute("SELECT * FROM Employees WHERE Email=%s", (email,))
            user = cur.fetchone()
            role = "staff" if user else None

        if not user:
            flash("No account found with this email. Please register first.", "error")
            return render_template("register_and_signin.html", mode="login", email=email)
        
       
        # Check password
        if not bcrypt.checkpw(password.encode("utf-8"), user["Password_Hash"].encode("utf-8")):
            flash("Incorrect password. Please try again.", "error")
            return render_template("register_and_signin.html", mode="login", email=email)

        # Successful login → store session
        session.clear()
        if role == "customer":
            session["user_id"] = user["CustomerID"]
            session["account_number"] = user["Account_Number"]
            session["role"] = "Customer"
            
        else:
            session["user_id"] = user["EmployeeID"]
            session["role"] = user.get("Role", "Staff")

        session["email"] = user["Email"]
        session["type"] = role
        session["user_name"] = user.get("First_Name", "User")

        flash(f"Welcome back, {session['user_name']}!", "success")
        return redirect(url_for("index"))
    
        
    except Exception as e:
        flash(f"Login failed: {e}", "error")
        return render_template("register_and_signin.html", mode="login", email=email)

    finally:
        cur.close()
        conn.close()


# ------------------------
# Logout
# ------------------------
@auth_bp.get("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

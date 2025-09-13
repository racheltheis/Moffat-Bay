# =====================================================
# 🔹 Backend Logic
# =====================================================

import sqlite3
from flask import Flask, render_template, session, redirect, url_for, flash, request
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key"  # change in production
DATABASE = "moffat_bay.db"

# ---- Database Connection ----
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ---- Landing Page (Available Rooms) ----
@app.route("/")
def landing():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rooms WHERE available = 1")
    rooms = cur.fetchall()
    conn.close()

    return render_template("landing.html", rooms=rooms)


# ---- Reservation Booking (POST) ----
@app.route("/reserve/<int:room_id>", methods=["POST"])
def reserve(room_id):
    if "user_id" not in session:
        flash("Please log in to make a reservation.")
        return redirect(url_for("login"))

    checkin = request.form.get("checkin")
    checkout = request.form.get("checkout")

    if not checkin or not checkout:
        flash("Check-in and check-out dates are required.")
        return redirect(url_for("landing"))

    conn = get_db_connection()
    cur = conn.cursor()

    # Create reservation
    cur.execute("""
        INSERT INTO reservations (customer_id, room_id, checkin, checkout, status)
        VALUES (?, ?, ?, ?, 'confirmed')
    """, (session["user_id"], room_id, checkin, checkout))

    # Mark room as unavailable
    cur.execute("UPDATE rooms SET available = 0 WHERE room_id = ?", (room_id,))

    conn.commit()
    conn.close()

    flash("Reservation successful!")
    return redirect(url_for("dashboard"))


# ---- Dashboard (User Profile + Reservations + Payments + Reviews) ----
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("You must be logged in first.")
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor()

    # Get user info
    cur.execute("SELECT * FROM customers WHERE customer_id = ?", (session["user_id"],))
    user = cur.fetchone()

    # Get reservations
    cur.execute("""
        SELECT r.reservation_id, rm.room_number, rm.room_type, rm.price, 
               r.checkin, r.checkout, r.status
        FROM reservations r
        JOIN rooms rm ON r.room_id = rm.room_id
        WHERE r.customer_id = ?
        ORDER BY r.checkin DESC
    """, (session["user_id"],))
    reservations = cur.fetchall()

    # Get payments
    cur.execute("""
        SELECT p.payment_id, p.amount, p.payment_date, p.method, p.status
        FROM payments p
        JOIN reservations r ON p.reservation_id = r.reservation_id
        WHERE r.customer_id = ?
    """, (session["user_id"],))
    payments = cur.fetchall()

    # Get reviews
    cur.execute("""
        SELECT rv.review_id, rv.rating, rv.comment, rv.review_date, rm.room_number
        FROM reviews rv
        JOIN rooms rm ON rv.room_id = rm.room_id
        WHERE rv.customer_id = ?
    """, (session["user_id"],))
    reviews = cur.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        user=user,
        reservations=reservations,
        payments=payments,
        reviews=reviews
    )
    
    # ---- Submit Review ----
@app.route("/review/<int:reservation_id>", methods=["POST"])
def review(reservation_id):
    if "user_id" not in session:
        flash("You must be logged in to leave a review.")
        return redirect(url_for("login"))

    rating = request.form.get("rating")
    comment = request.form.get("comment")

    if not rating:
        flash("Rating is required.")
        return redirect(url_for("dashboard"))

    conn = get_db_connection()
    cur = conn.cursor()

    # Get room tied to reservation
    cur.execute("SELECT room_id FROM reservations WHERE reservation_id = ? AND customer_id = ?", 
                (reservation_id, session["user_id"]))
    res = cur.fetchone()

    if not res:
        flash("Invalid reservation.")
        conn.close()
        return redirect(url_for("dashboard"))

    room_id = res["room_id"]

    # Insert review
    cur.execute("""
        INSERT INTO reviews (customer_id, room_id, rating, comment)
        VALUES (?, ?, ?, ?)
    """, (session["user_id"], room_id, rating, comment))

    conn.commit()
    conn.close()

    flash("Thank you for your review!")
    return redirect(url_for("dashboard"))

# --- About Us Page --- 
@app.route("/about")
    def about():   
        return render_template("about.html")
    
# --- Summary Page --- 
@app.route("/summary")
def summary():
    conn = get_db_connection()
    cur = conn.cursor()

    # Total customers
    cur.execute("SELECT COUNT(*) FROM customers")
    total_customers = cur.fetchone()[0]

    # Total reservations
    cur.execute("SELECT COUNT(*) FROM reservations")
    total_reservations = cur.fetchone()[0]

    # Total revenue (completed payments only)
    cur.execute("SELECT IFNULL(SUM(amount), 0) FROM payments WHERE status = 'completed'")
    total_revenue = cur.fetchone()[0]

    # Average review rating
    cur.execute("SELECT ROUND(AVG(rating), 1) FROM reviews")
    avg_rating = cur.fetchone()[0] or 0

    # Available rooms
    cur.execute("SELECT COUNT(*) FROM rooms WHERE available = 1")
    available_rooms = cur.fetchone()[0]

    conn.close()

    return render_template(
        "summary.html",
        total_customers=total_customers,
        total_reservations=total_reservations,
        total_revenue=total_revenue,
        avg_rating=avg_rating,
        available_rooms=available_rooms
    )


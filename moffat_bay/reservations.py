# reservations.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_conn
from datetime import datetime

res_bp = Blueprint("res", __name__, url_prefix="/reservations")

# -----------------------------
# RESERVATIONS (use reservations.html)
# -----------------------------
@res_bp.get("/")
def reservation_get():
    # Optional: prefetch available rooms from DB
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT RoomID, Room_Type, Price_Per_Night, Max_Guests, Status FROM Rooms")
    rooms = cur.fetchall()
    cur.close(); conn.close()
    return render_template("reservations.html", rooms=rooms)

@res_bp.post("/")
def reservation_post():
    if "user_id" not in session:
        flash("Please log in to book a room.", "error")
        return redirect(url_for("auth.login_get"))

    # Values from reservations.html
    check_in = request.form.get("check_in")
    check_out = request.form.get("check_out")
    adults = request.form.get("adults")
    children = request.form.get("children")
    room_type = request.form.get("room_type")  # you’ll need hidden input or JS for room selection

    # validate dates
    try:
        ci = datetime.strptime(check_in, "%m/%d/%Y").date()
        co = datetime.strptime(check_out, "%m/%d/%Y").date()
        if ci >= co:
            raise ValueError("Check-out must be after check-in.")
    except Exception as e:
        flash(f"Invalid dates: {e}", "error")
        return redirect(url_for("res.reservation_get"))

    conn = get_conn(); cur = conn.cursor(dictionary=True)
    try:
        # Ensure a room of that type is available
        cur.execute("SELECT RoomID, Price_Per_Night, Status FROM Rooms WHERE Room_Type=%s LIMIT 1", (room_type,))
        room = cur.fetchone()
        if not room or room["Status"] != "Available":
            flash("Selected room not available.", "error")
            return redirect(url_for("res.reservation_get"))

        guests = int(adults or 1) + int(children or 0)
        nights = (co - ci).days
        total_price = room["Price_Per_Night"] * nights

        # Insert reservation
        cur.execute(
            """
            INSERT INTO Reservations (CustomerID, RoomID, Check_In_Date, Check_Out_Date, Num_Guests, Total_Price, Status)
            VALUES (%s, %s, %s, %s, %s, %s, 'Pending')
            """,
            (session["user_id"], room["RoomID"], ci, co, guests, total_price)
        )
        reservationid = cur.lastrowid
        conn.commit()

        return redirect(url_for("res.confirm_get", reservationid=reservationid))

    except Exception as e:
        conn.rollback()
        flash(f"Booking failed: {e}", "error")
        return redirect(url_for("res.reservation_get"))
    finally:
        cur.close(); conn.close()

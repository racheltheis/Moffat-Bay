# reservations.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_conn
from datetime import datetime

# Blueprint name is "res", everything lives under /reservations
res_bp = Blueprint("res", __name__, url_prefix="/reservations")

# -----------------------------
# GET: reservations page (form + room list)
# -----------------------------
@res_bp.get("/")
def reservations():
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT RoomID, Room_Type, Price_Per_Night, Max_Guests, Status FROM Rooms")
    rooms = cur.fetchall()
    cur.close(); conn.close()
    return render_template("reservations.html", rooms=rooms)

# -----------------------------
# POST: handle reservation form submit
# -----------------------------
@res_bp.post("/")
def reservations_post():
    if "user_id" not in session:
        flash("Please log in to book a room.", "error")
        return redirect(url_for("auth.login_get"))

    # Values from reservations.html
    check_in = request.form.get("check_in")
    check_out = request.form.get("check_out")
    adults = request.form.get("adults")
    children = request.form.get("children")
    room_type = request.form.get("room_type")  # hidden input or JS selection

    # validate dates
    try:
        ci = datetime.strptime(check_in, "%Y-%m-%d").date()
        co = datetime.strptime(check_out, "%Y-%m-%d").date()
        if ci >= co:
            raise ValueError("Check-out must be after check-in.")
    except Exception as e:
        flash(f"Invalid dates: {e}", "error")
        return redirect(url_for("res.reservations"))

    conn = get_conn(); cur = conn.cursor(dictionary=True)
    try:
        # Ensure a room of that type is available
        cur.execute("SELECT RoomID, Price_Per_Night, Status FROM Rooms WHERE Room_Type=%s AND Status = 'Available' LIMIT 1", (room_type,))
        room = cur.fetchone()
        if not room:
            flash("Selected room type is not available.", "error")
            return redirect(url_for("res.reservations"))

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

        # redirect to confirmation page
        return redirect(url_for("res.confirm_get", reservationid=reservationid))

    except Exception as e:
        conn.rollback()
        flash(f"Booking failed: {e}", "error")
        return redirect(url_for("res.reservations"))
    finally:
        cur.close(); conn.close()

# -----------------------------
# GET: confirm page
# -----------------------------
@res_bp.get("/confirm/<int:reservationid>")
def confirm_get(reservationid):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT r.ReservationID, r.Check_In_Date, r.Check_Out_Date, r.Num_Guests, r.Total_Price, r.Status,
               rm.Room_Type, rm.Price_Per_Night,
               c.First_Name, c.Last_Name, c.Email, c.Phone as Phone_Number
        FROM Reservations r
        JOIN Rooms rm ON rm.RoomID = r.RoomID
        JOIN Customers c ON c.CustomerID = r.CustomerID
        WHERE r.ReservationID=%s
    """, (reservationid,))
    res = cur.fetchone()
    cur.close()
    conn.close()

    if not res:
        flash("Reservation not found.", "error")
        return redirect(url_for("res.reservations"))
    
    # Separate variables for template
    name = f"{res['First_Name']} {res['Last_Name']}"
    phone = res.get("Phone_Number", "")
    email = res["Email"]
    checkin = res["Check_In_Date"].strftime("%Y-%m-%d")
    checkout = res["Check_Out_Date"].strftime("%Y-%m-%d")
    adults = res["Num_Guests"]
    children = 0
    room_type = res["Room_Type"]
    price = res["Price_Per_Night"]
    total = res["Total_Price"]
   
    return render_template(
        "confirm.html",
        name=name,
        phone=phone,
        email=email,
        checkin=checkin,
        checkout=checkout,
        adults=adults,
        children=children,
        room_type=room_type,
        price=price,
        total=total,
        reservationid=reservationid
    )

@res_bp.route("/confirm/<int:reservationid>", methods=["POST"])
def confirm_post(reservationid):
    action = request.form.get("action")
    if action == "submit":
        flash("Reservation confirmed!", "success")
    elif action == "cancel":
        flash("Reservation canceled.", "warning")
    return redirect(url_for("res.reservations"))

# ----------------------------------------
# --- NEW: MY RESERVATIONS PAGE ---
# ----------------------------------------
@res_bp.get("/my-reservations")
def my_reservations():
    """
    Shows a list of all reservations for the currently logged-in customer.
    """
    # Ensure a customer is logged in
    if "user_id" not in session or session.get("type") != "customer":
        flash("Please log in to view your reservations.", "error")
        return redirect(url_for("auth.login_get"))

    customer_id = session["user_id"]
    reservations = []
    try:
        conn = get_conn()
        cur = conn.cursor(dictionary=True)
        # Query for all reservations belonging to this customer
        cur.execute("""
            SELECT r.ReservationID, r.Check_In_Date, r.Check_Out_Date, r.Status, r.Total_Price,
                   rm.Room_Type
            FROM Reservations r
            JOIN Rooms rm ON rm.RoomID = r.RoomID
            WHERE r.CustomerID = %s
            ORDER BY r.Check_In_Date DESC
        """, (customer_id,))
        reservations = cur.fetchall()
    except Exception as e:
        flash(f"An error occurred while fetching your reservations: {e}", "error")
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'conn' in locals() and conn:
            conn.close()
    
    # You will need to create a my_reservations.html template for this
    return render_template("my_reservations.html", reservations=reservations)

# -----------------------------
# LOOKUP (for general use)
# -----------------------------
@res_bp.route("/lookup", methods=["GET", "POST"])
def lookup():
    """
    Allows any user to look up a reservation by EITHER Reservation ID or Email.
    """
    results, q = None, ""
    if request.method == "POST":
        q = request.form.get("query", "").strip()
        conn = get_conn(); cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT r.ReservationID, r.Check_In_Date, r.Check_Out_Date, r.Status, r.Total_Price,
                   rm.Room_Type, c.Email
            FROM Reservations r
            JOIN Rooms rm ON rm.RoomID = r.RoomID
            JOIN Customers c ON c.CustomerID = r.CustomerID
            WHERE r.ReservationID = %s OR c.Email = %s
        """, (q, q))
        results = cur.fetchall()
        cur.close(); conn.close()

    return render_template("lookup.html", results=results, query=q)

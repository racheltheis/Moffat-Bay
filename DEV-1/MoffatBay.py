import mysql.connector 
import bcrypt

# Connect to MySQL (update with your credentials)
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",       # change to your MySQL username
    password="pass"    # change to your MySQL password
)

cursor = conn.cursor()

# Step 1: Create Database
cursor.execute("DROP DATABASE IF EXISTS MoffatBay;")
cursor.execute("CREATE DATABASE IF NOT EXISTS MoffatBay;")
cursor.execute("USE MoffatBay;")

# Step 2: Create Tables in correct order
tables = [
    """
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INT AUTO_INCREMENT PRIMARY KEY,
        Account_Number VARCHAR(20) UNIQUE,
        First_Name VARCHAR(50),
        Last_Name VARCHAR(50),
        Email VARCHAR(100) UNIQUE,
        Password_Hash VARCHAR(255),
        Phone VARCHAR(20),
        Created_At DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Employees (
        EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
        First_Name VARCHAR(50),
        Last_Name VARCHAR(50),
        Email VARCHAR(100) UNIQUE,
        Password_Hash VARCHAR(255),
        Phone VARCHAR(20),
        Role ENUM('Staff', 'Admin'),
        Created_At DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Rooms (
        RoomID INT AUTO_INCREMENT PRIMARY KEY,
        Room_Number VARCHAR(10) UNIQUE,
        Room_Type VARCHAR(50),
        Description TEXT,
        Max_Guests INT,
        Price_Per_Night DECIMAL(10,2),
        Status ENUM('Available', 'Reserved', 'Maintenance'),
        Image_url VARCHAR(255)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Reservations (
        ReservationID INT AUTO_INCREMENT PRIMARY KEY,
        CustomerID INT,
        RoomID INT,
        Check_In_Date DATE,
        Check_Out_Date DATE,
        Num_Guests INT,
        Total_Price DECIMAL(10,2),
        Status ENUM('Pending', 'Confirmed', 'Cancelled'),
        Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE,
        FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Payments (
        PaymentID INT AUTO_INCREMENT PRIMARY KEY,
        ReservationID INT,
        Amount DECIMAL(10,2),
        Payment_Method ENUM('Credit_Card', 'Debit_Card', 'Paypal'),
        Payment_Status ENUM('Paid', 'Failed', 'Refunded'),
        Payment_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ReservationID) REFERENCES Reservations(ReservationID)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Reviews (
        ReviewID INT AUTO_INCREMENT PRIMARY KEY,
        CustomerID INT,
        RoomID INT,
        Rating INT CHECK (Rating BETWEEN 1 AND 5),
        Comment TEXT,
        Review_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE,
        FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Staff_Notes (
        NoteID INT AUTO_INCREMENT PRIMARY KEY,
        ReservationID INT,
        EmployeeID INT,
        Note_Text TEXT,
        Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ReservationID) REFERENCES Reservations(ReservationID) ON DELETE CASCADE,
        FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID) ON DELETE CASCADE
    );
    """
]

for t in tables:
    cursor.execute(t)

# Step 3: Insert sample data with bcrypt hashed passwords
def hash_password(plain):
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# Customers
customer_data = [
    ('CUST1001', 'Annie', 'Johansson', 'alice.johansson@email.com', 'Alice1234', '952-199-1234'),
    ('CUST1002', 'Michael', 'Lee', 'michael.lee@email.com', 'Michael123', '207-888-6789'),
    ('CUST1003', 'Victor', 'Lopez', 'victor.lopez@email.com', 'Victor123', '952-097-9876')
]

for acc_num, first, last, email, pwd, phone in customer_data:
    cursor.execute(
        "INSERT INTO Customers (Account_Number, First_Name, Last_Name, Email, Password_Hash, Phone) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (acc_num, first, last, email, hash_password(pwd), phone)
    )

# Employees
employee_data = [
    ('Joel', 'Smith', 'joel.smith@moffatbay.com', 'Joel12345', '763-109-1122', 'Staff'),
    ('Kendra', 'Watson', 'kendra.watson@moffatbay.com', 'Kendra123', '218-615-3344', 'Admin'),
    ('Michelle', 'Taylor', 'michelle.taylor@moffatbay.com', 'Michelle123', '612-003-5566', 'Staff')
]

for first, last, email, pwd, phone, role in employee_data:
    cursor.execute(
        "INSERT INTO Employees (First_Name, Last_Name, Email, Password_Hash, Phone, Role) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (first, last, email, hash_password(pwd), phone, role)
    )

# Rooms
cursor.executemany("""
    INSERT INTO Rooms (Room_Number, Room_Type, Description, Max_Guests, Price_Per_Night, Status, Image_url)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""", [
    ('111', 'Double Full Beds', 'Double beds with patio view', 4, 120.00, 'Available', 'room111.jpg'),
    ('112', 'Queen Bed', 'Queen bed with ocean view', 2, 135.00, 'Reserved', 'room112.jpg'),
    ('211', 'Double Queen Beds', 'Double queen beds with patio view', 4, 150.00, 'Available', 'suite211.jpg'),
    ('212', 'King Bed', 'King bed with ocean view', 2, 160.00, 'Maintenance', 'suite212.jpg')
])

# Reservations
cursor.executemany("""
    INSERT INTO Reservations (CustomerID, RoomID, Check_In_Date, Check_Out_Date, Num_Guests, Total_Price, Status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""", [
    (1, 1, '2025-09-01', '2025-09-03', 2, 360.00, 'Confirmed'),
    (2, 2, '2025-09-10', '2025-09-17', 2, 810.00, 'Pending'),
    (3, 3, '2025-09-15', '2025-09-20', 3, 640.00, 'Cancelled')
])

# Payments
cursor.executemany("""
    INSERT INTO Payments (ReservationID, Amount, Payment_Method, Payment_Status)
    VALUES (%s, %s, %s, %s)
""", [
    (1, 450.00, 'Credit_Card', 'Paid'),
    (2, 675.00, 'Paypal', 'Failed'),
    (3, 160.00, 'Debit_Card', 'Refunded')
])

# Reviews
cursor.executemany("""
    INSERT INTO Reviews (CustomerID, RoomID, Rating, Comment)
    VALUES (%s, %s, %s, %s)
""", [
    (1, 1, 5, 'We loved our stay at Moffat Bay! The staff was fantastic!'),
    (2, 2, 4, 'The ammentities were great!'),
    (3, 3, 3, 'We liked the location and amenities, but thought our room felt outdated.')
])

# Staff Notes
cursor.executemany("""
    INSERT INTO Staff_Notes (ReservationID, EmployeeID, Note_Text)
    VALUES (%s, %s, %s)
""", [
    (1, 1, 'Guest requests early check-in (1pm).'),
    (2, 3, 'Guest requests a call to discuss check in on 9/1.'),
    (3, 2, 'Guest is celebrating 1st wedding anniversary.')
])

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("Database, tables, and sample data created successfully with hashed passwords!")

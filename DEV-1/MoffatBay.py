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
cursor.execute("drop DATABASE IF EXISTS MoffatBay;")
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

# You can keep the rest of your sample inserts for Rooms, Reservations, Payments, Reviews, Staff_Notes
# ...

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("Database and tables created successfully with hashed passwords!")

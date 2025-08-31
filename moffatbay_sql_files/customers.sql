USE MoffatBay;

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

INSERT INTO Customers (Account_Number, First_Name, Last_Name, Email, Password_Hash, Phone)
VALUES
('CUST1001', 'Annie', 'Johansson', 'alice.johansson@email.com', 'Argon2a', '952-199-1234'),
('CUST1002', 'Michael', 'Lee', 'michael.lee@email.com', 'Argon2b', '207-888-6789'),
('CUST1003', 'Victor', 'Lopez', 'victor.lopez@email.com', 'Argon2c', '952-097-9876');
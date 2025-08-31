USE MoffatBay;

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

INSERT INTO Employees (First_Name, Last_Name, Email, Password_Hash, Phone, Role)
VALUES
('Joel', 'Smith', 'joel.smith@moffatbay.com', 'Argon2d', '763-109-1122', 'Staff'),
('Kendra', 'Watson', 'kendra.watson@moffatbay.com', 'Argon2e', '218-615-3344', 'Admin'),
('Michelle', 'Taylor', 'michelle.taylor@moffatbay.com', 'Argon2f', '612-003-5566', 'Staff');
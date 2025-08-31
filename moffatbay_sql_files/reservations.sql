USE MoffatBay;

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
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID)
);

INSERT INTO Reservations (CustomerID, RoomID, Check_In_Date, Check_Out_Date, Num_Guests, Total_Price, Status)
VALUES
(1, 1, '2025-09-01', '2025-09-03', 2, 360.00, 'Confirmed'),
(2, 2, '2025-09-10', '2025-09-17', 2, 810.00, 'Pending'),
(3, 3, '2025-09-15', '2025-09-20', 3, 640.00, 'Cancelled');
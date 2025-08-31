USE MoffatBay;

CREATE TABLE IF NOT EXISTS Payments (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    ReservationID INT,
    Amount DECIMAL(10,2),
    Payment_Method ENUM('Credit_Card', 'Debit_Card', 'Paypal'),
    Payment_Status ENUM('Paid', 'Failed', 'Refunded'),
    Payment_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ReservationID) REFERENCES Reservations(ReservationID)
);

INSERT INTO Payments (ReservationID, Amount, Payment_Method, Payment_Status)
VALUES
(1, 450.00, 'Credit_Card', 'Paid'),
(2, 675.00, 'Paypal', 'Failed'),
(3, 160.00, 'Debit_Card', 'Refunded');
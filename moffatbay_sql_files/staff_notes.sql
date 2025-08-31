USE MoffatBay;

CREATE TABLE IF NOT EXISTS Staff_Notes (
    NoteID INT AUTO_INCREMENT PRIMARY KEY,
    ReservationID INT,
    EmployeeID INT,
    Note_Text TEXT,
    Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ReservationID) REFERENCES Reservations(ReservationID),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
);

INSERT INTO Staff_Notes (ReservationID, EmployeeID, Note_Text)
VALUES
(1, 1, 'Guest requests early check-in (1pm).'),
(2, 3, 'Guest requests a call to discuss check in on 9/1.'),
(3, 2, 'Guest is celebrating 1st wedding anniversary.');
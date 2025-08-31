USE MoffatBay;

CREATE TABLE IF NOT EXISTS Reviews (
    ReviewID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    RoomID INT,
    Rating INT CHECK (Rating BETWEEN 1 AND 5),
    Comment TEXT,
    Review_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID)
);

INSERT INTO Reviews (CustomerID, RoomID, Rating, Comment)
VALUES
(1, 1, 5, 'We loved our stay at Moffat Bay! The staff was fantastic!'),
(2, 2, 4, 'The ammentities were great!'),
(3, 3, 3, 'We liked the location and amenities, but thought our room felt outdated.');
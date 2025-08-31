USE MoffatBay;

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

INSERT INTO Rooms (Room_Number, Room_Type, Description, Max_Guests, Price_Per_Night, Status, Image_url)
VALUES
('111', 'Double Full Beds', 'Double beds with patio view', 4, 120.00, 'Available', 'room111.jpg'),
('112', 'Queen Bed', 'Queen bed with ocean view', 2, 135.00, 'Reserved', 'room112.jpg'),
('211', 'Double Queen Beds', 'Double queen beds with patio view', 4, 150.00, 'Available', 'suite211.jpg');
('212', 'King Bed', 'King bed with ocean view', 2, 160.00, 'Maintenance', 'suite212.jpg');
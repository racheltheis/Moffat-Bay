-- Moffat Bay Lodge Database Schema
DROP TABLE IF EXISTS staff_notes;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS attractions;

-- Customers 
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    password TEXT NOT NULL,         -- hashed password for login
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Employees (lodge staff, admins)
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL,             -- e.g., 'front_desk', 'manager'
    password TEXT NOT NULL,         -- hashed password for staff login
    hired_date DATE DEFAULT CURRENT_DATE
);

-- Rooms (hotel rooms available to book)
CREATE TABLE rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_number TEXT NOT NULL UNIQUE,
    room_type TEXT NOT NULL,        -- Single, Double, Suite
    price REAL NOT NULL,
    capacity INTEGER NOT NULL,
    available INTEGER DEFAULT 1     -- 1 = available, 0 = occupied
);

-- Reservations (bookings by customers)
CREATE TABLE reservations (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    checkin DATE NOT NULL,
    checkout DATE NOT NULL,
    status TEXT DEFAULT 'confirmed', -- confirmed, cancelled, checked_in, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(room_id) REFERENCES rooms(room_id)
);

-- Payments (linked to reservations)
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reservation_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    method TEXT NOT NULL,            -- card, cash, online
    status TEXT DEFAULT 'completed', -- completed, pending, failed
    FOREIGN KEY(reservation_id) REFERENCES reservations(reservation_id)
);

-- Reviews (guests leave feedback after stay)
CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    comment TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(room_id) REFERENCES rooms(room_id)
);


-- Staff Notes (internal lodge communication)
CREATE TABLE staff_notes (
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    reservation_id INTEGER,
    note TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY(reservation_id) REFERENCES reservations(reservation_id)
);

-- Seed sample rooms
INSERT INTO rooms (room_number, room_type, price, capacity, available) VALUES
('101', 'Single', 100.00, 1, 1),
('102', 'Double', 150.00, 2, 1),
('201', 'Suite', 250.00, 4, 1);

-- Attractions (things to do around the lodge)
CREATE TABLE attractions (
    attraction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    short_description TEXT,
    image_url TEXT
);

-- Seed sample attractions -- 
INSERT INTO attractions (name, short_description, image_url) VALUES
('Kayaking Tours', 'Guided kayak tours exploring the bay.', 'kayaking.jpg'),
('Hiking Trails', '25 miles of scenic hiking trails.', 'hiking.jpg'),
('Whale Watching', 'Seasonal tours with marine life sightings.', 'whale_watching.jpg'),
('Scuba Diving', 'Excursions for all skill levels.', 'scuba_diving.jpg');
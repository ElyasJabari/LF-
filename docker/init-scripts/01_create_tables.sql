-- Table for holding static data for devices
CREATE TABLE ref_device (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Insert sample data into ref_device
INSERT INTO ref_device (name)
VALUES
    ('Mobile'),
    ('Desktop'),
    ('Laptop'),
    ('Tablet');

-- Table for holding static data for categories
CREATE TABLE ref_category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Insert sample data into ref_category
INSERT INTO ref_category (name)
VALUES
    ('Buying'),
    ('Returns'),
    ('Login'),
    ('Payment'),
    ('History');

-- Table for holding static data for statuses
CREATE TABLE ref_status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Insert sample data into ref_status
INSERT INTO ref_status (name)
VALUES
    ('Open'),
    ('Closed'),
    ('Not Reproducible');

-- Table for holding variable data for tickets
CREATE TABLE tbl_ticket (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    creation_date TIMESTAMP NOT NULL,
    due_date TIMESTAMP,
    device_id INT REFERENCES ref_device(id),
    category_id INT REFERENCES ref_category(id),
    status_id INT REFERENCES ref_status(id),
    CONSTRAINT fk_device FOREIGN KEY (device_id) REFERENCES ref_device(id),
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES ref_category(id),
    CONSTRAINT fk_status FOREIGN KEY (status_id) REFERENCES ref_status(id)
);

-- Table for user roles
CREATE TABLE ref_role (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Inserting predefined roles into ref_role table
INSERT INTO ref_role (name) VALUES ('Technician'), ('Support');

-- Table for users
CREATE TABLE tbl_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL, -- Consider using a secure hashing algorithm for passwords
    role_id INTEGER REFERENCES ref_role(id) NOT NULL
);


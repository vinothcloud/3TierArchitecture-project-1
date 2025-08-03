show DATABASES;

use fbdatabase;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL
);

INSERT INTO users (username, password, email) 
VALUES 
('vinothfb', 'Sensitive123#', 'vinoth@example.com'),
('vijay', 'vijay123', 'vijay@example.com'),
('Surya', 'Surya123', 'surya@example.com');

SELECT * FROM users;
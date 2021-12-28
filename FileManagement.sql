CREATE DATABASE FileManagement;
USE FileManagement;

CREATE USER dbadmin IDENTIFIED BY 'helloworld';
GRANT ALL ON FileManagement .* TO 'dbadmin'@'%';
FLUSH PRIVILEGES;

CREATE TABLE Registration(
usn_ssid CHAR(10) PRIMARY KEY,
Username VARCHAR(25) UNIQUE NOT NULL,
Email VARCHAR(320) UNIQUE NOT NULL,
Pass VARCHAR(15) NOT NULL,
Branch VARCHAR(50),
College VARCHAR(50) NOT NULL,
CONSTRAINT username_check CHECK (Username NOT LIKE '%[^A-Z0-9_]%'),
CONSTRAINT email_check CHECK (Email LIKE '%___@___%.__%')
);

DESC Registration;


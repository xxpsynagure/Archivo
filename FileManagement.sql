CREATE DATABASE FileManagement;
USE FileManagement;

CREATE USER dbadmin IDENTIFIED BY 'helloworld';
GRANT ALL ON FileManagement .* TO 'dbadmin'@'%';
FLUSH PRIVILEGES;

CREATE TABLE Registration(
usn_ssid CHAR(10) PRIMARY KEY,
Username VARCHAR(30) UNIQUE NOT NULL,
Email VARCHAR(255) UNIQUE NOT NULL,
Pass VARCHAR(255) NOT NULL,
Branch VARCHAR(255),
College VARCHAR(255) NOT NULL,
CONSTRAINT username_check CHECK (Username NOT LIKE '%[^A-Z0-9_]%'),
CONSTRAINT email_check CHECK (Email LIKE '%___@___%.__%')
);

DESC Registration;
SHOW TABLES;

SELECT * FROM Registration;

CREATE TABLE College(
College_id VARCHAR(10) PRIMARY KEY,
College_name VARCHAR(255) NOT NULL);

INSERT INTO College VALUES('SJEC', 'St. Joseph Engineering College, Mangalore');
INSERT INTO College VALUES('SCEM', 'Sahyadri College of Engineering and Management, Mangalore');
INSERT INTO College VALUES('SDM', 'S.D.M. Institute of Technology, Ujire');
INSERT INTO College VALUES('CEC', 'Canara Engineering College, Mangalore');
INSERT INTO College VALUES('VCET', 'Vivekananda College of Engineering and Technology, Puttur');

CREATE TABLE Branch(
Branch_id VARCHAR(10),
Branch_name VARCHAR(255) NOT NULL,
College_id VARCHAR(10) REFERENCES College(College_id),
PRIMARY KEY(Branch_id, College_id));

INSERT INTO Branch VALUES('CIV','Civil Engineering','SJEC');
INSERT INTO Branch VALUES('CSE','Computer Science and Engineering','SJEC');
INSERT INTO Branch VALUES('EEE','Electrical and Electronics Engineering','SJEC');
INSERT INTO Branch VALUES('ECE','Electronics and Communication Engineering','SJEC');
INSERT INTO Branch VALUES('ME','Mechanical Engineering','SJEC');

show tables;
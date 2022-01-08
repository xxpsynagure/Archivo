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
T_or_S CHAR(1) NOT NULL,
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

CREATE TABLE Teacher (
    ssid CHAR(10) PRIMARY KEY,
    Fname VARCHAR(255) NOT NULL,
    Lname VARCHAR(255) NOT NULL,
    Designation VARCHAR(255) NOT NULL,
    Department VARCHAR(50) NOT NULL,
    yr_of_exp NUMERIC(2) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Phno NUMERIC(13) NOT NULL,
    Skills VARCHAR(255),
    Image BLOB,
    FOREIGN KEY (ssid) REFERENCES Registration (usn_ssid)
)

CREATE TABLE Student (
    usn VARCHAR(10) PRIMARY KEY,
    Fname VARCHAR(255) NOT NULL,
    Lname VARCHAR(255) NOT NULL,
    Branch VARCHAR(50) NOT NULL,
    Sem NUMERIC(1) NOT NULL,
    Sec CHAR(1) NOT NULL,
    DOB DATE NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Phno NUMERIC(13) NOT NULL,
    Image BLOB,
    Portfolio_links VARCHAR(500),
    About VARCHAR(700),
    FOREIGN KEY (usn) REFERENCES Registration (usn_ssid)
)

CREATE TABLE Subject (
    ssid VARCHAR(10) NOT NULL,
    Branch VARCHAR(50) NOT NULL,
    Sem NUMERIC(1) NOT NULL,
    Sec CHAR(1) NOT NULL,
    Subject_code VARCHAR(6) NOT NULL,
    Subject_name VARCHAR(50),
    FOREIGN KEY (ssid) REFERENCES Teacher (ssid),
    FOREIGN KEY (Branch) REFERENCES Student (Branch),
    FOREIGN KEY (Sem) REFERENCES Student (Sem),
    FOREIGN KEY (Sec) REFERENCES Student (Sec)
)

CREATE TABLE Notification (
    ssid VARCHAR(10) PRIMARY KEY,
    Branch VARCHAR(50) NOT NULL,
    Sem NUMERIC(1) NOT NULL,
    Sec CHAR(1) NOT NULL,
    Date DATE PRIMARY KEY,
    Time TIMESTAMP PRIMARY KEY,
    Message VARCHAR(1000) NOT NULL,
    FOREIGN KEY (ssid) REFERENCES Teacher (ssid),
    FOREIGN KEY (Branch) REFERENCES Subject (Branch),
    FOREIGN KEY (Sem) REFERENCES Subject (Sem),
    FOREIGN KEY (Sec) REFERENCES Subject (Sec)
)

CREATE TABLE Repository (
    Repoid VARCHAR(13) PRIMARY KEY,
    usn VARCHAR(10) NOT NULL,
    Reponame VARCHAR(255) NOT NULL,
    Date_created DATE,
    Date_last_modified DATE,
    Time_created TIME,
    Time_last_modified Time,
    FOREIGN KEY (usn) REFERENCES Student (usn)
)

CREATE TABLE File (
    Repoid VARCHAR(13) PRIMARY KEY,
    Filename VARCHAR(255) PRIMARY KEY,
    Filetype VARCHAR(20) PRIMARY KEY,
    Content VARCHAR(20000),
    Date_created DATE,
    Date_last_modified DATE,
    Time_created TIME,
    Time_last_modified TIME,
    FOREIGN KEY (Repoid) REFERENCES Repository (Repoid)
)
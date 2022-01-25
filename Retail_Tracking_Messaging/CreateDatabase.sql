CREATE TABLE "Customer_Table" (
	"CustomerID"	INTEGER NOT NULL,
	"Username"	TEXT,
	"Password"	TEXT,
	"Forename"	TEXT,
	"Surname"	TEXT,
	"Email"	TEXT,
	"DeliveryAddress"	TEXT,
	PRIMARY KEY("CustomerID" AUTOINCREMENT)
);

CREATE TABLE "Employee_Table" (
	"EmployeeID"	INTEGER NOT NULL,
	"Username"	TEXT,
	"Password"	TEXT,
	"Forename"	TEXT,
	"Surname"	TEXT,
	PRIMARY KEY("EmployeeID" AUTOINCREMENT)
);

CREATE TABLE "Message_Table" (
	"MessageID"	INTEGER NOT NULL,
	"CustomerID"	INTEGER,
	"EmployeeID"	INTEGER,
	"FromName"	TEXT,
	"ToName"	TEXT,
	"MessageText"	TEXT,
	"Product"	INTEGER,
	"Timestamp"	TEXT,
	FOREIGN KEY("CustomerID") REFERENCES "Customer_Table"("CustomerID"),
	FOREIGN KEY("EmployeeID") REFERENCES "Employee_Table"("EmployeeID"),
	PRIMARY KEY("MessageID" AUTOINCREMENT)
);
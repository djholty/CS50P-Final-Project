import sqlite3

#SETUP SQLITE CURSOR

conn = sqlite3.connect('ledgerdb.sqlite')
cur = conn.cursor()

#DELETE TABLES IF THEY EXIST

cur.execute('DROP TABLE IF EXISTS Children')
cur.execute('DROP TABLE IF EXISTS Workbooks')
cur.execute('DROP TABLE IF EXISTS Members')

# CREATE TABLES

cur.execute('''CREATE TABLE "Children" (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE)''')

#INSERT NAMES INTO CHILDREN TABLE

cur.execute(''' INSERT INTO Children (name) VALUES ('River')''')
cur.execute(''' INSERT INTO Children (name) VALUES ('Summer')''')

#CREATE WORKBOOKS TABLE

cur.execute(''' CREATE TABLE "Workbooks" (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT
    )''')

#CREATE MEMBERS TABLE TO DEAL WITH MANY TO MANY RELATIONSHIP OF CHILDREN TO WORKBOOKS

cur.execute(''' CREATE TABLE "Members" (
    children_id INTEGER,
    workbooks_id INTEGER,
    completed INTEGER,
    date TEXT,
    PRIMARY KEY (children_id, workbooks_id)
    )''')

#POPULATE WORKBOOK TABLE WITH TITLES

workbooks = [('Grade 1 Writing'),('Grade 1 Reading'),('Grade 1 Word Problems'),('Grade 1 Geometry and Measurement'),
('Grade 1 Addition'),('Grade 1 Subtraction'),('Grade 2 Writing'),('Grade 2 Reading'),('Grade 2 Word Problems'),
('Grade 2 Geometry and Measurement'),('Grade 2 Addition'),('Grade 2 Subtraction')]
cur.executemany("INSERT INTO Workbooks VALUES (?,)" ,workbooks)


cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 3 Writing')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 3 Reading')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 3 Word Problems')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 3 Geometry and Measurement')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 3 Addition and Subtraction')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 3 Multiplication')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 3 Division')''')

cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 4 Writing')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 4 Reading')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 4 Word Problems')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 4 Geometry and Measurement')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 4 Multiplication')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 4 Division')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 4 Decimals and Fractions')''')

cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 5 Writing')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 5 Reading')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 5 Word Problems')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 5 Geometry and Measurement')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 5 Decimals and Fractions')''')

cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 6 Writing')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 6 Reading')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 6 Word Problems')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 6 Geometry and Measurement')''')
cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 6 Fractions')''')



conn.commit()



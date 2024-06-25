import pytest
import project
import sqlite3
from unittest.mock import Mock 

cur = None
conn = None

@pytest.fixture
def setup():
    global cur
    global conn
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    
    #DELETE TABLES IF THEY EXIST

    cur.execute('DROP TABLE IF EXISTS Children')
    cur.execute('DROP TABLE IF EXISTS Workbooks')
    cur.execute('DROP TABLE IF EXISTS Members')
    cur.execute('DROP TABLE IF EXISTS Account')

    #CREATE CHILDREN TABLE

    cur.execute('''CREATE TABLE IF NOT EXISTS "Children" (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE)''')

    #CREATE WORKBOOKS TABLE

    cur.execute(''' CREATE TABLE IF NOT EXISTS "Workbooks" (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT
        )''')

    #CREATE MEMBERS TABLE TO DEAL WITH MANY TO MANY RELATIONSHIP OF CHILDREN TO WORKBOOKS

    cur.execute(''' CREATE TABLE IF NOT EXISTS "Members" (
        children_id INTEGER,
        workbooks_id INTEGER,
        completed INTEGER,
        date TEXT,
        PRIMARY KEY (children_id, workbooks_id)
        )''')

    #CREATE ACCOUNT TABLE

    cur.execute(''' CREATE TABLE IF NOT EXISTS "Account" (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        children_id INTEGER,
        date TEXT,
        description TEXT,
        amount REAL
        )''')

    #POPULATE CHILDREN TABLE

    cur.execute(''' INSERT OR IGNORE INTO Children (name) VALUES ('River')''')
    cur.execute(''' INSERT OR IGNORE INTO Children (name) VALUES ('Summer')''')

    #POPULATE WORKBOOKS TABLE WITH WORKBOOK NAMES    

    cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 1 Writing')''')
    cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 1 Reading')''')
    cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 1 Word Problems')''')
    cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 1 Geometry and Measurement')''')
    cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 1 Addition')''')
    cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 1 Subtraction')''')

    cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 2 Writing')''')
    cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 2 Reading')''')
    cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 2 Word Problems')''')
    cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 2 Geometry and Measurement')''')
    cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 2 Addition')''')
    cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 2 Subtraction')''')

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

    #POPULATE MEMBERS TABLE WITH 4 COMPLETED WORKBOOKS
    completedwb = [
    (2,5,1,'2020-03-01'),
    (2, 6, 1,'2020-06-24'),
    (1,17,1,'2020-06-24'),
    (1,9,1,'2020-07-29')
    ]

    cur.executemany("""INSERT INTO Members VALUES (?,?,?,?)""", completedwb)

    #POPULATE ACCOUNT TABLE WITH 4 TRANSACTIONS
    transactions = [
    (1, '2021-03-04', 'Kung Fu XP', 80.00),
    (2, '2021-03-04', 'Kung Fu XP', 30.00),
    (1, '2021-03-11', 'Completed Grade 4 Reading', 25.00),
    (2, '2021-04-12', 'Purchase Fountain Pen', -45.00),
    ]

    cur.executemany("""INSERT INTO Account (children_id, date, description, amount) 
    VALUES (?,?,?,?)""", transactions)

    conn.commit()
    yield cur
    conn.close()



    
    #sqlite function to get id of last_insert_rowid

def test_view_completed_workbooks(setup):
    cur = setup
    items = project.view_completed_workbooks(1, cur)
    assert len(items) == 2

def test_get_child_transactions(setup):
    cur = setup
    items = project.get_child_transactions(1, cur)
    assert len(items) == 2

def test_get_date(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "2022-10-12")
    assert project.get_date() == "2022-10-12"

def test_insert_new_transaction(setup, monkeypatch):
    cur = setup
    cur.execute("""SELECT * FROM Account""")
    items = cur.fetchall()
    assert len(items) == 4
    
    inputs = iter(['2022-12-22', 'Test', 1])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    project.insert_new_transaction(1,cur)
    conn.commit()
    cur.execute("""SELECT * FROM Account""")
    items = cur.fetchall()
    assert len(items) == 5

def test_insert_new_completedwkbook(setup, monkeypatch):
    cur = setup
    cur.execute("""SELECT * FROM Members""")
    items = cur.fetchall()
    assert len(items) == 4
    inputs = iter(['2022-12-22', 26])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    project.insert_new_completedwkbook(1, cur)
    cur.execute("""SELECT * FROM Members""")
    items = cur.fetchall()
    assert len(items) == 5


    
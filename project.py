import sqlite3
import sys



def main():
    global conn 
    global cur
    
    while True:
        print("""
        Welcome to the ledger.  Here you can select your child and view or record completed workbooks.
        You may also record purchases and rewards, as well as list recent transactions by child.
        Please select the child for which you would like to view or record new entries. 

        Menu:
        (1) Choose a Child
        (2) Exit
        """)

        menu1 = input("Please insert your menu number: ")

        if menu1 == '1':
            # Retrieve List of Children From Children Table
            conn = sqlite3.connect('ledgerdb.sqlite')
            cur = conn.cursor()
            cur.execute('''SELECT rowid, Children.name FROM Children''')
            items = cur.fetchall()
            conn.close()

    
            #create a list to contain all the children available and add all children to it
            numbers = []
            children = []
            for item in items:
                number, child = item
                numbers.append(number)
                print(f'({number})  {child}')
                
                
                
            while True:
                #get all the numbers that correspond to the kid
                   
                child_id = input("Please Select the number of your Child from those listed: ")
                if int(child_id) not in numbers:
                    print('Invalid selection, please select a number from the list')
                    continue
            
                #if selected child available view new child menu
                else:
                    
                    while True:
                        print(""" 
                        Menu:
                        (1) Insert a new completed workbook
                        (2) Insert a new transaction
                        (3) View all completed workbooks
                        (4) View all recent transactions
                        (5) Exit
                        
                        """)
                        menu2 = input("Please Enter a menu option: ")
                        while True: 

                            if menu2 == '1':
                                conn = sqlite3.connect('ledgerdb.sqlite')
                                cur = conn.cursor()
                                insert_new_completedwkbook(child_id, cur)
                                conn.commit()
                                conn.close()
                                break
                            elif menu2 == '2':
                                conn = sqlite3.connect('ledgerdb.sqlite')
                                cur = conn.cursor()
                                insert_new_transaction(child_id, cur)
                                conn.commit()
                                conn.close()
                                break
                            elif menu2 == '3':
                                conn = sqlite3.connect('ledgerdb.sqlite')
                                cur = conn.cursor()
                                view_completed_workbooks(child_id, cur)
                                conn.close()
                                break
                            elif menu2 =='4':
                                
                                conn = sqlite3.connect('ledgerdb.sqlite')
                                cur = conn.cursor()
                                get_child_transactions(child_id, cur)
                                conn.close()
                                break
                            elif menu2 == '5':
                                print('Thanks for using the ledger, God be with you.')
                                sys.exit()
                            else:
                                print('Invalid Menu Option, please try again')
                                break
        elif menu1 == '2':
            print("Thank you for using the ledger.  God be with you.")
            sys.exit()
        else:
            print()
            print('Invalid Selection, Please choose a number')
            continue

#function for inserting a newly completed workbook
def insert_new_completedwkbook(child_id, cur):
    date = get_date()
    workbooknum = choose_workbook(cur)
    
    print()
    print(f'Inserting Child ID: {child_id} Date Completed: {date} Workbook Number: {workbooknum}')
    cur.execute("""INSERT OR IGNORE INTO Members (children_id, workbooks_id, completed, date) VALUES (?,?,?,?)""",(child_id, workbooknum, 1, date) )
    print("************************************")
    print("Transaction inserted successfully")


# Get the appropriate workbook ID from the list in table
def choose_workbook(cur)-> int:
    
    cur.execute("""SELECT * from Workbooks""")
    items = cur.fetchall()
    
    # Print all workbook titles with ID no.
    for item in items:
        number, title = item
        print(f'ID Number: {number}         Title: {title}')


    #picking a valid id number thats in the range of the list
    while True:
        titleno = input("Please pick the ID number of your title: ")
        try:
            titleno = int(titleno)
            if titleno in range(1,len(items)+1):
                return titleno
            else:
                print("Invalid ID Number")
                continue
        except:
            print("Invalid input")
            continue

#Get appropriately formatted date for inserting new record
def get_date()-> str:
    while True:
        date = input("Please insert the transaction date in the following format YYYY-MM-DD: ")
        try:
            year, month, day = date.split('-')
            if len(year) == 4 and len(month) == 2 and len(day) == 2:
                try:
                    year = int(year)
                    month =  int(month)
                    day = int(day)
                    if month > 12 or day > 31:
                        print("Invalid MM or DD")
                        continue
                    else:
                        return date
                except:
                    print('Invalid formatting, please input as YYYY-MM-DD')
                    continue
            else:
                print("Invalid formatting, please input as YYYY-MM-DD")
                continue        
        except:
            print('Invalid formatting, please input as YYYY-MM-DD')
            continue

#function for inserting a new transaction purchase or withdrawal
def insert_new_transaction(child_id, cur):
    
    date = get_date()
    while True:
        description = input('Please enter a text description of the Transaction: ')
        if len(description) > 59:
            print("Please shorten the description to less than 60 characters")
            continue
        else:
            break
    #Error checking for amount
    while True:
        amount = input("Please enter the amount of the transaction (negative numbers for withdrawals):")
        try:
            amount = float(amount)
            break
        except:
            print("Invalid format, please enter a number")
            continue
    print()
    
    print(f'Child ID: {child_id} Date: {date} Description: {description} Amount: {amount}')
    cur.execute("""INSERT OR IGNORE INTO Account (children_id, date, description, amount) VALUES (?,?,?,?)""",(child_id, date, description, amount) )
    print(f'Inserted the following: ChildID: {child_id} Date: {date} Descr: {description} Amount: {amount}' )
    print("Transaction inserted successfully")
    

def view_completed_workbooks(child_id, cur):
    #GET ALL COMPLETED WORKBOOKS ORDERED BY WORKBOOK NAME

    
    cur.execute('''SELECT Children.name, Workbooks.name, Members.completed, Members.date
    FROM Children JOIN Workbooks JOIN Members ON Children.id = Members.children_id 
    AND Workbooks.id = Members.workbooks_id WHERE Children.id = ? ORDER BY Members.date''', (child_id,))

    items = cur.fetchall()
    # debugging
    for item in items:
        child, workbook, completed, date = item
        print(f'{child}  {workbook:40} {date:10}')
    return items

def get_child_transactions(child_id, cur):
    
    cur.execute('''SELECT Children.name, Account.date, Account.description, Account.amount
    FROM Children JOIN Account ON Children.id = Account.children_id WHERE Children.id = ?
    ORDER BY Children.name, Account.Date''', (child_id,))

    items = cur.fetchall()
    cumtot = 0
    for item in items:
        name, date, descr, amount = item
        cumtot = amount + cumtot
        print(f'{name}    {date}    {descr:58}    Amount:{amount:6.2f}   Cumulative Total:{cumtot:.2f}')

    return items

#SETUP SQLITE CURSOR

# #DELETE TABLES IF THEY EXIST

# cur.execute('DROP TABLE IF EXISTS Children')
# cur.execute('DROP TABLE IF EXISTS Workbooks')
# cur.execute('DROP TABLE IF EXISTS Members')
# cur.execute('DROP TABLE IF EXISTS Account')

# CREATE TABLES

# cur.execute('''CREATE TABLE IF NOT EXISTS "Children" (
#     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#     name TEXT UNIQUE)''')

#INSERT NAMES INTO CHILDREN TABLE

# cur.execute(''' INSERT OR IGNORE INTO Children (name) VALUES ('River')''')
# cur.execute(''' INSERT OR IGNORE INTO Children (name) VALUES ('Summer')''')

#CREATE WORKBOOKS TABLE

# cur.execute(''' CREATE TABLE IF NOT EXISTS "Workbooks" (
#     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#     name TEXT
#     )''')

#CREATE MEMBERS TABLE TO DEAL WITH MANY TO MANY RELATIONSHIP OF CHILDREN TO WORKBOOKS

# cur.execute(''' CREATE TABLE IF NOT EXISTS "Members" (
#     children_id INTEGER,
#     workbooks_id INTEGER,
#     completed INTEGER,
#     date TEXT,
#     PRIMARY KEY (children_id, workbooks_id)
#     )''')

# cur.execute(''' CREATE TABLE IF NOT EXISTS "Account" (
#     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#     children_id INTEGER,
#     date TEXT,
#     description TEXT,
#     amount REAL
#     )''')


#POPULATE WORKBOOK TABLE WITH TITLES

# workbooks = [
#     ('Grade 1 Writing',),
#     ('Grade 1 Reading',),
#     ('Grade 1 Word Problems',),
#     ('Grade 1 Geometry and Measurement',),
#     ('Grade 1 Addition',),
#     ('Grade 1 Subtraction',)
# 
# 
# 
# ]

# cur.executemany('''INSERT OR IGNORE INTO Workbooks (name) VALUES (?)''', workbooks)
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 1 Writing')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 1 Reading')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 1 Word Problems')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 1 Geometry and Measurement')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 1 Addition')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 1 Subtraction')''')

# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 2 Writing')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 2 Reading')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 2 Word Problems')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 2 Geometry and Measurement')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 2 Addition')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 2 Subtraction')''')

# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 3 Writing')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 3 Reading')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 3 Word Problems')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 3 Geometry and Measurement')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 3 Addition and Subtraction')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 3 Multiplication')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 3 Division')''')

# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 4 Writing')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 4 Reading')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 4 Word Problems')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 4 Geometry and Measurement')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 4 Multiplication')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 4 Division')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 4 Decimals and Fractions')''')

# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 5 Writing')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 5 Reading')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 5 Word Problems')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 5 Geometry and Measurement')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 5 Decimals and Fractions')''')

# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 6 Writing')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 6 Reading')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 6 Word Problems')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 6 Geometry and Measurement')''')
# cur.execute('''INSERT INTO Workbooks (name) VALUES ('Grade 6 Fractions')''')


# #POPULATE MEMBERS TABLE WITH CHILD AND COMPLETED WORKBOOKS AND DATES

# completedwb = [
# (2,5,1,'2020-03-01'),
# (2, 6, 1,'2020-06-24'),
# (1,17,1,'2020-06-24'),
# (2,4,1,'2020-07-15'),
# (1,19,1,'2020-07-15'),
# (1,9,1,'2020-07-29'),
# (2,1,1,'2020-09-10'),
# (1,24,1,'2020-09-10'),
# (1,13,1,'2020-11-20'),
# (2,11,1,'2020-12-01'),
# (1,16,1,'2021-01-23'),
# (1,21,1,'2021-03-11'),
# (1,22,1,'2021-04-18'),
# (1,23,1,'2021-05-08'),
# (1,20,1,'2021-06-16'),
# (2,9,1,'2021-08-10'),
# (2,10,1,'2021-08-10'),
# (1,28,1,'2021-08-20'),
# (1,26,1,'2021-09-30'),
# (2,18,1,'2021-10-15'),
# (1,30,1,'2021-11-26'),
# (2,17,1,'2022-01-07'),
# (1,29,1,'2022-01-16'),
# (1,27,1,'2022-05-15'),
# (2,19,1,'2022-06-11'),
# (2,7,1,'2022-07-15')
# ]
# cur.executemany("""INSERT INTO Members VALUES (?,?,?,?)""", completedwb)
# print("Members table populated with completed workbooks")


# transactions = [
# (1, '2021-03-04', 'Kung Fu XP', 80.00),
# (2, '2021-03-04', 'Kung Fu XP', 30.00),
# (1, '2021-03-11', 'Completed Grade 4 Reading', 25.00),
# (2, '2021-04-12', 'Purchase Fountain Pen', -45.00),
# (1, '2021-04-19', 'Completed Grade 4 Word Problems', 25.00),
# (1, '2021-04-29', 'Purchase Thea Stilton Book', -11.00),
# (1, '2021-05-08', 'Completed Grade 4 Geometry and Measurement', 25.00),
# (1, '2021-06-16', 'Completed Grade 4 Writing', 25.00),
# (2, '2021-08-10', 'Completed Grade 2 Work Problems', 25.00),
# (2, '2021-08-10', 'Completed Grade 2 Geometry and Measurement', 25.00),
# (1, '2021-08-10', 'Babulian Form Complete', 20.00),
# (2, '2021-08-10', 'Babulian Form Complete', 20.00),
# (1, '2021-08-10', 'Stopped Chewing Nails', 15.00),
# (1, '2021-08-14', 'Won Chapters Gift Card for Study', 25.00),
# (2, '2021-08-14', 'Won Chapters Gift Card for Study', 25.00),
# (1, '2021-08-20', 'Completed Grade 5 Reading', 25.00),
# (2, '2021-09-04', 'Headband Purchase', -25.00),
# (2, '2021-09-17', 'UV Pen Purchase', -3.50),
# (1, '2021-09-17', 'Scholastic Book order and UV Pen', -22.50),
# (1, '2021-09-25', 'Kung Fu XP 18k-28k', 100.00),
# (2, '2021-09-25', 'Kung Fu XP 18k-28k', 100.00),
# (1, '2021-09-30', 'Completed Grade 5 Decimals and Fractions', 25.00),
# (1, '2021-10-08', 'Completed Piano Book', 25.00),
# (2, '2021-10-15', 'Completed Grade 3 Multiplication', 25.00),
# (2, '2021-10-20', 'Cozy Grotto', -17.00),
# (2, '2021-11-02', 'Halloween Candy Buyback', 23.50),
# (1, '2021-11-02', 'Halloween Candy Buyback', 23.50),
# (1, '2021-11-26', 'Completed Geometry and Measurement', 25.00),
# (2, '2021-12-17', 'Necklace Purchase', -30.00),
# (2, '2021-12-17', 'Lost tooth', 5.00),
# (2, '2021-12-26', 'Horse Stickers', -5.00),
# (1, '2021-12-27', 'Kung Fu XP 20k-30k', 100.00),
# (2, '2021-12-27', 'Kung Fu XP 20k-30k', 100.00),
# (2, '2021-12-27', 'Washii Tape', -15.00),
# (2, '2022-01-07', 'Completed Grade 3 Addition/Subtraction', 25.00),
# (2, '2022-01-07', 'Lost front tooth', 25.00),
# (1, '2022-01-16', 'Completed Grade 5 Word Problems', 25.00),
# (1, '2022-02-01', 'Chinese New Year', 20.00),
# (2, '2022-02-01', 'Chinese New Year', 20.00),
# (1, '2022-02-01', 'Bare Minimum Workbooks January 2022', 20.00),
# (2, '2022-02-01', 'Bare Minimum Workbooks January 2022', 20.00),
# (1, '2022-03-09', 'Disneyland Unspent Spending Money', 20.00),
# (2, '2022-03-09', 'Necklace and pins from Disneyland beyond spending money', -25),
# (1, '2022-03-19', 'Cozy Grotto', -2),
# (2, '2022-03-19', 'Cozy Grotto and Jewelry', -22.50),
# (2, '2022-04-01', 'Lost Tooth', 5.00),
# (2, '2022-04-01', 'Bare Minimum Workbooks March 2022', 20.00),
# (1, '2022-04-01', 'Bare Minimum Workbooks March 2022', 20.00),
# (1, '2022-05-02', 'Bare Minimum Workbooks April 2022', 20.00),
# (2, '2022-05-02', 'Bare Minimum Workbooks April 2022', 20.00),
# (1, '2022-05-15', 'Completed Grade 5 Writing', 25.00),
# (2, '2022-05-15', 'Lost tooth', 25.00),
# (1, '2022-05-26', 'Lost tooth', 5.00),
# (1, '2022-06-04', 'Bare Minimum Workbooks May 2022', 20.00),
# (2, '2022-06-04', 'Bare Minimum Workbooks May 2022', 10.00),
# (2, '2022-06-11', 'Completed Grade 3 Division', 25.00),
# (2, '2022-06-11', 'Snake stuffy and stickers', -19.00),
# (2, '2022-07-10', 'Sunglasses, Markers, Stickers', -50.00),
# (2, '2022-07-15', 'Completed Writing Grade 2', 25.00),
# (1, '2022-07-15', 'Bare Minimum Workbooks June 2022', 10.00),
# (2, '2022-07-15', 'Bare Minimum Workbooks June 2022', 10.00)
# ]

# #POPULATE ACCOUNT TABLE WITH OLD TRANSACTIONS

# cur.executemany("""INSERT INTO Account (children_id, date, description, amount) VALUES (?,?,?,?)""", transactions)
# conn.commit()
# conn.close()
# print("Account Table populated with data")




if __name__ == "__main__":
    main()

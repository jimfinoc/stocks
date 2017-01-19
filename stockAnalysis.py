import sqlite3
from yahoo_finance import Share
import os.path

# check to see if the database file exist and if not, create it.
sqlite_file = 'my_stocks.sqlite'
if os.path.isfile(sqlite_file):
    print "File looks like it exist."
else: #create the File
    print "Creating the database."
    sqlite_file = 'my_stocks.sqlite'    # name of the sqlite database file
    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE transactions (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    action TEXT,
    type TEXT,
    stock TEXT,
    date TEXT,
    comission REAL,
    fees REAL,
    price REAL,
    quantity INTEGER)
    ''')
    conn.commit()
    conn.close()


if os.path.isfile(sqlite_file):
    sqlite_file = 'my_stocks.sqlite'    # name of the sqlite database file
    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    print "Please enter the data for the stock purchase."
    dateInput = raw_input("Date in format of (2016-12-31):").upper()
    actionInput = raw_input('Action (BUY or SELL):').upper()
    stockInput = raw_input("Stock symbol (F):").upper()
    typeInput = raw_input("Commodity (STOCK):").upper()
    priceInput = float(raw_input("Transaction Price (10.00):"))
    comissionInput = float(raw_input("Comission costs (8.00):"))
    feesInput = float(raw_input("Fees (1.00):"))
    quantityInput = int(raw_input("Quantity traded (100):"))
    # Do this instead
    print "Your transaction is as follows:"
    statement = (actionInput, typeInput, stockInput, dateInput, comissionInput, feesInput, priceInput, quantityInput)
    print statement
    c.execute('INSERT INTO transactions VALUES (NULL,?,?,?,?,?,?,?,?)', statement)
    conn.commit()
    conn.close()
else: #create the File
    print "Something is wrong with the file."

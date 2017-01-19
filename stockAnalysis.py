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
    id INTEGER PRIMARY KEY,
    transactionType TEXT,
    stock TEXT,
    transactionDate TEXT,
    comission REAL,
    fees REAL,
    price REAL,
    quantity INTEGER)
    ''')
    conn.commit()
    conn.close()

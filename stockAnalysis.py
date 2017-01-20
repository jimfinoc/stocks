import sqlite3
from yahoo_finance import Share
import os.path
import datetime

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
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    action TEXT,
    type TEXT,
    stock TEXT,
    date TEXT,
    comission REAL,
    fees REAL,
    price REAL,
    quantity INTEGER,
    total REAL)
    ''')
    conn.commit()
    conn.close()

def refresh_positions():
    #SELECT DISTINCT stock FROM transactions
    #
    #For stockSymbol each loop
    #   lets add up shares and totals and get price per share
    #   SELECT * FROM transactions WHERE stock = stockSymbol
    #
    #   lets look up price per share
    #   data = Share(stockSymbol)
    #   data.get_price()
    pass

def add_transaction():
    if os.path.isfile(sqlite_file):
        # Connecting to the database file
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        print "Please enter the data for the stock purchase."
        while True:
            dateInput = raw_input("Date in format of (2016-12-31):")
            try:
                dateValue = datetime.datetime.strptime(dateInput,"%Y-%m-%d")
                break
            except:
                try:
                    dateValue = datetime.datetime.strptime(dateInput,"%b %d, %Y")
                    break
                except:
                    try:
                        dateValue = datetime.datetime.strptime(dateInput,"%d %b %Y")
                        break
                    except:
                        try:
                            dateValue = datetime.datetime.strptime(dateInput,'%m/%d/%Y')
                            break
                        except:
                            try:
                                dateValue = datetime.datetime.strptime(dateInput,'%m/%d/%y')
                                break
                            except:
                                print "I don't understand that date, please try again."
        print "I think your date is: ", str(dateValue.date())
        actionInput = ""
        while actionInput == "":
            actionInput = raw_input('Action (BUY or SELL):').upper()
        stockInput = ""
        while stockInput == "":
            stockInput = raw_input("Stock symbol (F):").upper()
        typeInput = raw_input("Commodity (STOCK):").upper()
        if typeInput == "":
            typeInput = "STOCK"
            print "We'll assume you meant STOCK"
        while True:
            try:
                priceInput = float(raw_input("Transaction Price (10.00):"))
                break
            except:
                print "Please enter the price."
        try:
            comissionInput = float(raw_input("Comission costs (8.95):"))
        except:
            print "we'll just assume you meant 8.95"
            comissionInput = float(8.95)
        try:
            feesInput = float(raw_input("Fees (0.00):"))
        except:
            print "we'll just assume you meant 0.00"
            feesInput = float(0.00)
        while True:
            try:
                quantityInput = int(raw_input("Quantity traded (100):"))
                break
            except:
                print "I'm going to need you to try that again"
        if actionInput == "BUY":
            total = quantityInput * priceInput + comissionInput + feesInput
        elif actionInput == "SELL":
            total = quantityInput * priceInput - comissionInput - feesInput
        print "Your transaction is as follows:"
        statement = (actionInput, typeInput, stockInput, str(dateValue.date()), comissionInput, feesInput, priceInput, quantityInput, total)
        print statement
        c.execute('INSERT INTO transactions VALUES (NULL,?,?,?,?,?,?,?,?,?)', statement)
        conn.commit()
        conn.close()
    else: #create the File
        print "Something is wrong with the file."

while True:
    print "You're in the stock program. Time to make some money!"
    print ""
    print "Your current positions are as follow:"
    refresh_positions()
    # print "THE POSITIONS"
    print ("""
    1. View transaction list
    2. Add a transaction
    3. Quit
    """)
    ans=raw_input("What would you like to do? ")
    if ans=="1":
        pass
    elif ans=="2":
        add_transaction()
    elif ans=="3":
        print("\n Goodbye")
        break
    elif ans !="":
        print("\n Not Valid Choice Try again")

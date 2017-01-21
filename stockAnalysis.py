import csv
import sqlite3
from yahoo_finance import Share
import os.path
import datetime

# check to see if the database file exist and if not, create it.
sqlite_file = 'my_stocks.sqlite'
import_file = "import_stock.csv"

if os.path.isfile(sqlite_file):
    # print "File looks like it exist."
    pass
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
    if os.path.isfile(sqlite_file):
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        c.execute('SELECT DISTINCT stock FROM transactions')
        print c.fetchall()
        conn.commit()
        conn.close()
    else: #create the File
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
                                try:
                                    dateValue = datetime.datetime.strptime(dateInput,"%d-%b-%Y")
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
            total = round(quantityInput * priceInput + comissionInput + feesInput,2)
        elif actionInput == "SELL":
            total = round(quantityInput * priceInput - comissionInput - feesInput,2)
        print "Your transaction is as follows:"
        statement = (actionInput, typeInput, stockInput, str(dateValue.date()), comissionInput, feesInput, priceInput, quantityInput, total)
        print statement
        c.execute('INSERT INTO transactions VALUES (NULL,?,?,?,?,?,?,?,?,?)', statement)
        conn.commit()
        conn.close()
    else: #create the File
        print "Something is wrong with the file."

def import_transactions():
    if os.path.isfile(sqlite_file) and os.path.isfile(import_file):
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        print "Please ensure your data is in a comma seperated value format of"
        print "Action, Type, Symbol, Date, Price, Quantity, Comission, & Fees"
        print "or as an example:"
        print "BUY, STOCK, F, 2016-12-31, 10.00, 1000, 8.95, 0"
        print "the file should be named import_stock.csv"
        print ""
        print "the statement will be recorded as follows:"
        print "(actionInput, typeInput, stockInput, date, comissionInput, feesInput, priceInput, quantityInput, total)"
        with open(import_file, 'rb') as f:
            data = csv.reader(f)
            for row in data:
                # print row
                actionInput = row[0].upper()
                typeInput = row[1].upper().replace(" ","",1)
                stockInput = row[2].upper().replace(" ","",1)
                try:
                    dateValue = datetime.datetime.strptime(row[3].replace(" ","",1),"%Y-%m-%d")
                except:
                    dateValue = datetime.datetime.strptime(row[3].replace(" ","",1),"%d-%b-%y")
                priceInput = float(row[4].replace(" ","",1))
                quantityInput = int(row[5].replace(" ","",1))
                comissionInput = float(row[6].replace(" ","",1))
                feesInput = float(row[7].replace(" ","",1))
                if actionInput == "BUY":
                    total = round(quantityInput * priceInput + comissionInput + feesInput,2)
                elif actionInput == "SELL":
                    total = round(quantityInput * priceInput - comissionInput - feesInput,2)
                print "recorded: ",
                statement = (actionInput, typeInput, stockInput, str(dateValue.date()), comissionInput, feesInput, priceInput, quantityInput, total)
                print statement
                c.execute('INSERT INTO transactions VALUES (NULL,?,?,?,?,?,?,?,?,?)', statement)
        conn.commit()
        conn.close()

def view_transactions():
    if os.path.isfile(sqlite_file):
        # Connecting to the database file
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        c.execute('SELECT * FROM transactions')
        print c.fetchall()
        conn.commit()
        conn.close()
    else: #create the File
        print "Something is wrong with the file."



print "You're in the stock program. Time to make some money!"
while True:
    print ""
    print "Your current positions are as follow:"
    refresh_positions()
    # print "THE POSITIONS"
    print "1. View transaction list"
    print "2. Add a transaction"
    print "3. Import transactions from ", import_file
    print "Q. Quit"
    ans=raw_input("What would you like to do? ")
    if ans=="1":
        view_transactions()
    elif ans=="2":
        add_transaction()
    elif ans=="3":
        import_transactions()
    elif ans=="q" or ans=="Q":
        print("Goodbye")
        break
    elif ans !="":
        print("\n Not Valid Choice Try again")

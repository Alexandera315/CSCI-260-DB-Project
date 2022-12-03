import sqlite3
from sqlite3 import Error
from os import system, name

#Update tables

#Delete data from tables

#Log all changes made to file

#Menu interface for user

def create_connection(db_file):
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    
    
    return conn
            
def create_table(conn, create_table_sql):
  
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        
def displayTable(conn):
    
    table = getTableString()
        
    try:
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table}")
        
        rows = cur.fetchall()
        
        for row in rows:
            print(row)
    except Error as e:
        print(e)
        
def getTableString():
    print("Which table would you like to select? (1,2 or 3) ")
    Choice = input()

    table = ""
    if (int(Choice) == 1):
        table = "account"
    elif (int(Choice) == 2):
        table = "payment"
    else:
        table = "people"
        
    return table
        
def showMenu():
    print("Hello welcome to accounts payable")
    print("1) Create a new database")
    print("2) Display a table")
    print("3) Search a table")
    print("4) Update a customer, payment or account")
    print("5) Create a new customer, payment or account")
    print("6) Delete a customer, payment or account")
    print("7) Quit")
    choice = input()
    return choice
    
def clear():
    
    if name == 'nt':
        _ = system('cls')
        
    else:
        _ = system('clear')


def main():

    #database = r"C:\Users\User\Documents\SchoolDocuments\Python\Database\pythondb.db"
    #conn = create_connection(database)
    
    goOn = 0
    
    while (goOn != 1):
        choice = showMenu()
        
        if (int(choice) == 2):
            
            database = r"C:\Users\User\Documents\SchoolDocuments\Python\Database\pythondb.db"
            conn = create_connection(database)
            
            displayTable(conn)
        
        if (int(choice) == 7):
            quit()
            
        #0 Design and insert DB + Dummy data
        
        #1 1.Check if db already exsists
        #  2.Get DB name from user (filepath?)
        #  3.Make Database
        
        #3 1.Get table choice
        #  2.Search table choice based on relevant ID
        #  3.return result
        
        #4 1.Get table choice
        #  2.See number 3
        #  3.Edit result
    
    
    
    
if __name__ == '__main__':
    main()
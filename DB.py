#Alexander Apel

import strings
import sqlite3
from sqlite3 import Error
import os
from os import system, name
from os.path import exists as file_exists

DBfilePath = ""


def createDB():

    DBfilePath = os.getcwd() + "\\" + "pythondb.db"
    
    #Overall this function creates 3 tables for the intial db
    #The main part is using os.getcwd this is done in the current dir
    
    try:
        conn = create_connection(DBfilePath)
        create_table(conn,strings.intialDBStringAccount)
        create_table(conn,strings.intialDBStringPayment)
        create_table(conn,strings.intialDBStringPeople)
        input("Database created, Press enter to continue: ")
        clear()
    except Error as e:
        print("Sorry the database could not be created")
        print(e)

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
        
        rows = c.fetchall()
        
        for header in (strings.headerHeader[getTableValue(table) - 1]):
            print(header,"   ",end = "")
        
        print()
        
        for row in rows:
            print(row)
            
    except Error as e:
        print(e)
        
def searchTable(conn,searchString,tableID):
    
    #This function only works on the first column returned
    #WIll not work with a PK that is not the first value
    #in the column
    
    try:
        c = conn.cursor()
        c.execute(f"SELECT * FROM {tableID}")
        
        rows = c.fetchall()
        
    except Error as e:
        print(e)
         
    for row in rows:
            
        if (str(searchString) == str(row[0])):
            print(row)
    
#These next three functions are convience functions
#to convert accounts,payments,people = 1,2,3 
#and vice versa
#getTableString is used to query the user
    
def getTableString():
    print("Which table would you like to select? Account, Payment, People? (1,2,3): ")
    Choice = input()

    table = ""
    if (int(Choice) == 1):
        table = "Account"
    elif (int(Choice) == 2):
        table = "Payment"
    else:
        table = "People"
        
    return table
        
def getTableValue(string):
    if (string == "Account"):
        return 1
    elif ( string == "Payment"):
        return 2
    else:
        return 3
        
def getTableSearch(table):
    if (table == 2):
        return "payment_id"
    else:
        return "account_id"
        
def getConnection(string):
    conn = create_connection(string)
    return conn
                   
def showMenu():
    print("Hello welcome to accounts payable")
    print("1) Display a table")
    print("2) Search a table")
    print("3) Update a customer, payment or account")
    print("4) Create a new customer, payment or account")
    print("5) Delete a customer, payment or account")
    print("6) Quit")
    choice = input()
    return choice
    
def clear():
    
    #This function should be OS agnostic
    
    if name == 'nt':
        _ = system('cls')
        
    else:
        _ = system('clear')

def main():

    goOn = 0
    
    choice = 0
    
    while (goOn != 1):
        if (file_exists("pythondb.db")):
            choice = showMenu()
        else:
            createDB()
        
#-------------------------------------1      
        if (int(choice) == 1):
            
            conn = getConnection(os.getcwd() + "\\" + "pythondb.db")
            
            displayTable(conn)
            print()
            input("Press enter to continue ")
            clear()
            
#-------------------------------------2
        if (int(choice) == 2):
            table = getTableString()
            search = input("Please enter the ID you would like to search for: ")
            
            conn = getConnection(os.getcwd() + "\\" + "pythondb.db")
            
            searchTable(conn,search,table)
            
            print()
            input("Search Complete, Press enter to continue: ")
            clear()
            
#-------------------------------------3
        if (int(choice) == 3):
            table = getTableString()
            
            conn = getConnection(os.getcwd() + "\\" + "pythondb.db")
            
            yesOrNo = "n"
            
            sql2 = "SET "
            
            bucket = []
            
            #Holding pattern while user confirms their search value
            while (1 == 1):
                search = input("Please enter the ID you would like to update: ")
                
                searchTable(conn,search,table)
                
                yesOrNo = input("Is this the record you would like to modify? (y/n): ")
                
                if (yesOrNo == "y" or yesOrNo == "Y"):
                    break
             
            #These functions use the header values in STRINGS.py to read the correct values
            #and amount of values from the user for the given table
            for header in (strings.headerHeader[getTableValue(table) - 1]):
                bucket.append(input(f"New value for {header} ? "))
                
            for header in (strings.headerHeader[getTableValue(table) - 1]):
                sql2 = sql2 + header + "=" + bucket[0] + ","
                bucket.pop(0)
            
            sql2 = sql2[:-1] #This trims the last char by self assignment
            
            sql = f" UPDATE {table} {sql2} WHERE {strings.headerHeader[getTableValue(table) - 1][0]} = {search};"
            #strings.headerHeader[getTableValue(table) - 1][0] essentially fucntions to fetch the first 
            #header value for the given table
            
            with conn:
                try:
                    c = conn.cursor()
                    c.execute(sql)
                    input("Data updated succsessfully, press enter to continue ")
                except Error as e:
                    print(e)
            
            clear()
#-------------------------------------4   
        if (int(choice) == 4):
            table = getTableString()
            
            conn = getConnection(os.getcwd() + "\\" + "pythondb.db")
            
            
            sql2 = "("
            sql3 = "VALUES("
            bucket = []
            
            
            #These functions use the header values in STRINGS.py to read the correct values
            #and amount of values from the user for the given table
            #The first function querys values from the user
            #The second appends the header values for the Insert statment
            for header in (strings.headerHeader[getTableValue(table) - 1]):
                bucket.append(input(f"Value to insert for {header} ? "))
                
            for header in (strings.headerHeader[getTableValue(table) - 1]):
                sql2 = sql2 + header + ","
            
            #The below staments are SQL house keeping to assemble the query
            
            sql2 = sql2[:-1] #removes last charchters of string
            sql2 = sql2 + ")"
            
            for item in bucket: #paramtized insert function to avoid - and / in date values
                sql3 = sql3 + "?,"
                
            sql3 = sql3[:-1] #removes last charchters of string
            sql3 = sql3 + ");"
            
            sql = f"INSERT INTO {table} {sql2} {sql3}" #Query to insert
             
            with conn:
                try:
                    c = conn.cursor()
                    c.execute(sql,bucket) #paramtized insert function
                    input("Data inserted succsesfully, press enter to continue ")
                except Error as e:
                    print(e)
                    
            clear()
            
#-------------------------------------5   
        if (int(choice) == 5):
            table = getTableString()
            
            conn = getConnection(os.getcwd() + "\\" + "pythondb.db")
            
            while (1 == 1):
                search = input("Please enter the ID you would like to delete: ")
                
                searchTable(conn,search,table)
                
                yesOrNo = input("Is this the record you would like to modify? (y/n): ")
                
                if (yesOrNo == "y" or yesOrNo == "Y"):
                    break
                    
            sql = f"DELETE FROM {table} WHERE {strings.headerHeader[getTableValue(table) - 1][0]} = {search};"
            #strings.headerHeader[getTableValue(table) - 1][0] essentially fucntions to fetch the first 
            #header value for the given table
           
            with conn:
                try:
                    c = conn.cursor()
                    c.execute(sql)
                    input("Data deleted succsessfully, press enter to continue ")
                except Error as e:
                    print(e)
            
#-------------------------------------6       
        if (int(choice) == 6):
            clear()
            quit()

if __name__ == '__main__':
    main()
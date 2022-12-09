#These are the statments that are executed to create
#The database tables

intialDBStringAccount = """ 
    CREATE TABLE Account (
        account_id INT,
        balance DOUBLE,
        last_payment_date TEXT
    );
    """
    
intialDBStringPayment = """ 
    CREATE TABLE Payment (
        payment_id INT,
        account_id INT,
        amount DOUBLE,
        amount_sign BOOL,
        date_made TEXT
    );
    """
    
intialDBStringPeople = """ 
    CREATE TABLE People (
        account_id INT,
        first_name VARCHAR(20),
        last_name VARCHAR(20),
        phone_number VARCHAR(12)
    );
    """
    
accountHeader = ["account_id", "balance", "last_payment_date"]

paymentHeader = ["payment_id", "account_id","amount","amount_sign","date_made"]

peopleHeader = ["account_id", "first_name", "last_name", "phone_number"]

headerHeader = [accountHeader,paymentHeader,peopleHeader]

#These are the strings used by the modular functions to know what headers
#exsist within a table and gives a convient iterable for them
#The headerheader list exsists so the modular function knows which tables headers
#it needs to access
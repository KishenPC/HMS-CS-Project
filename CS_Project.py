def describe_table():
    conn_cursor = conn.cursor()
    table = input("Enter Name Of Table To Describe: ")
    conn_cursor.execute(f"DESCRIBE {table}")
    table_desc = conn_cursor.fetchall()
    columns = {} 
    print("The Format Is, {Column Name : Data Type}")
    for i in table_desc:
        columns.update({i[0]:i[1].upper()})
    print(f"{columns}\n")

def show_tables():
    conn_cursor = conn.cursor()
    conn_cursor.execute("SHOW TABLES")
    show_tables = conn_cursor.fetchall()
    tables = []
    for i in show_tables:
        for z in i: #Due to the fact that returned list of tables in the form [(t1,),(t2,)]
            tables.append(z)
    if len(tables) == 0:
        print("There Are No Available Tables in Your Database") 
    else:
        print("\t\t.___________________.")
        print("\t\tList of Tables\n")
        for i in tables:
            print(f"\t\t{tables.index(i)+1}| {i}")
        print("\t\t.___________________.")

def insert_values():
    table = input("Enter Table Name: ")
    entries = int(input("Enter Number Of Entries: "))
    print("The Columns Of The Table is as Follows: ")
    conn_cursor.execute(f"DESCRIBE {table}")
    table_desc = conn_cursor.fetchall()
    columns = {} 
    for i in table_desc:
        columns.update({i[0]:i[1].upper()})
    print(columns)
    for i in range(entries):
        entry = []
        for z in columns():
            x = input(f"Entry For Column {z}: ")
            if x.strip() == "":
                entry.append(NULL)
            else:
                entry.append(x)
        conn_cursor.execute(f"INSERT INTO {table} VALUES {entry}") #Look Through This (Subject to Errors)

        




import mysql.connector as sq
from mysql.connector import Error
from mysql.connector import errorcode

try:
    print("\n\t\t\tEnter SQL Server Connection Details")
    print("_"*91)
    host = input("Host Name: ")
    user = input("User Name: ")
    db = input("Database Name: ")
    passwd = input("Database Connection Password: ")
    conn = sq.connect(host=host, user=user , database=db, passwd=passwd)
    if conn.is_connected():
        print("\n✓ Database Connection Established! ✓")
        print("_"*91)
        print(f"\n-✧˖° Welcome To The {db} Databse Interface ˖°.✧-")
        show_tables()
        print("\n")
        while conn.is_connected():
            print("""Database Queries:-
            1. Describe a Table
            2. Insert A Value
            3. Close Connection""")
            action = input("\nEnter Command: ")
            if action.upper() == "CLOSE CONNECTION":
                conn.close()
            if action.upper() == "DESCRIBE A TABLE":
                describe_table()  
            if action.upper() == "INSERT A VALUE":
                insert_values()
            if action.upper() == "SELECT DATA" #Continue Here

except sq.Error:
    print("✘ Connection Failed! ✘")
    print(sq.Error)
    print("Make sure you have entered the right credentials for the database connection")

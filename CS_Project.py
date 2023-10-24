def describe_table():
    conn_cursor = conn.cursor()
    table = input("Enter Name Of Table To Describe: ")
    conn_cursor.execute(f"DESCRIBE {table}")
    table_desc = conn_cursor.fetchall()
    columns = {} 
    print("\nThe Format Is, {Column Name : Data Type}")
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
    conn.commit()

def insert_values():
    conn_cursor = conn.cursor()
    table = input("Enter Table Name: ")
    entries = int(input("Enter Number Of Entries: "))
    print("The Columns Of The Table is as Follows: ")
    conn_cursor.execute(f"DESCRIBE {table}")
    table_desc = conn_cursor.fetchall()
    columns = {} 
    for i in table_desc:
        columns.update({i[0]:i[1].upper()})
    print(f"{columns}\n")
    print("Enter The Values In Order Seperated By / ~ [A,B,C,1,2]")
    for i in range(entries):
        entry = tuple(input().split("/"))
        conn_cursor.execute(f"INSERT INTO {table} VALUES {entry}") #Under Maintenance
    conn.commit()
    

        
def create_hosptial_db():
    conn_cursor = conn.cursor()
    conn_cursor.execute("SHOW TABLES")
    show_tables = conn_cursor.fetchall()
    tables = []
    for i in show_tables:
        for z in i: #Due to the fact that returned list of tables in the form [(t1,),(t2,)]
            tables.append(z)
    if ('Patient', 'Doctor') in tables:
        print()
    else:
        conn_cursor.execute("CREATE TABLE Patient(Patient_ID INT PRIMARY KEY, Patient_Name VARCHAR(30), Patient_Gender VARCHAR(20), Address VARCHAR(50), Phone INT, Insurance_ID INT)")
        conn_cursor.execute("CREATE TABLE Doctor(Doctor_ID INT PRIMARY KEY, Doctor_Name VARCHAR(30), Specialization VARCHAR(30), Doctor_Gender VARCHAR(20), Address VARCHAR(50), Phone INT)") 
        

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
        print(f"\n-✧˖° Welcome To The HMS Databse Interface ˖°.✧-")
        create_hosptial_db()
        show_tables()
        
        while conn.is_connected():
            print("""\nDatabase Queries:-
            1. Table Details
            2. Record
            3. Disconnect""")
            action = input("\nEnter Command: ")
            if action.upper() == "DISCONNECT":
                conn.close()
            if action.upper() == "TABLE DETAILS":
                describe_table()
            if action.upper() == "RECORD DATA":
                insert_values()
                print("Values Recorded!\n")
            if action.upper() == "":
                pass #Continue Here

except sq.Error:
    print("\n✘ Connection Failed! ✘")
    print(sq.Error)
    print("Make sure you have entered the right credentials for the database connection")

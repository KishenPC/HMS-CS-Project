# Imports
import mysql.connector as sq
from getpass import getpass

# [!] - for errors
# [⁎] - for goods (i dont know what to write here)
# [#] - if something is not available or not found

# Functions
def describe_table():
    cursor = conn.cursor()
    table = input("(Enter Name Of Table To Describe) > ")
    cursor.execute(f"DESCRIBE {table}")
    table_desc = cursor.fetchall()
    columns = {} 
    print("\n[⁎] The Format Is, {Column Name : Data Type}")
    for i in table_desc:
        columns.update({i[0]:i[1].upper()})
    print(f"{columns}\n")

def show_tables():
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    show_tables = cursor.fetchall()
    tables = []
    for i in show_tables:
        for z in i: #Due to the fact that returned list of tables in the form [(t1,),(t2,)]
            tables.append(z)
    
    if len(tables) == 0:
        print("[#] There Are No Available Tables in Your Database") 
    else:
        print("\t\t.___________________.")
        print("\t\tList of Tables\n")
        for i in tables:
            print(f"\t\t{tables.index(i)+1}| {i}")
        print("\t\t.___________________.")

def insert_values():
    cursor = conn.cursor()
    table = input("(Enter Table Name) > ")
    entries = int(input("(Enter Number Of Entries) > "))

    print("[⁎] The Columns Of The Table is as Follows: ")
    cursor.execute(f"DESCRIBE {table}")
    table_desc = cursor.fetchall()
    columns = {} 
    for i in table_desc:
        columns.update({i[0]:i[1].upper()})
    print(columns)

    ent=[]
    for i in range(entries):
        entry = tuple(input("(Enter values) > ").split())
        ent.append(entry)
    cursor.executemany("INSERT INTO "+table+" VALUES(%s, %s, %s, %s, %s, %s)", ent)
    # %s is the no. of columns (you can change it according to the no. of columns)

    
    # this is just for the memes
    cursor.execute("SELECT * FROM " + table)
    item=cursor.fetchall()
    for a in item:
        print(a)
    ############################

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
        conn_cursor.execute("""CREATE TABLE Patient(
                            Patient_ID INT PRIMARY KEY,
                            Patient_Name VARCHAR(30),
                            Patient_Gender VARCHAR(20),
                            Address VARCHAR(50),
                            Phone INT,
                            Insurance_ID INT)""")
        
        conn_cursor.execute("""CREATE TABLE Doctor(
                            Doctor_ID INT PRIMARY KEY,
                            Doctor_Name VARCHAR(30),
                            Specialization VARCHAR(30),
                            Doctor_Gender VARCHAR(20),
                            Address VARCHAR(50),
                            Phone INT)""") 

# Code
print("\n"+"="*80)
print("  [Project] Hospital Management System")
print("="*80)

print("  [Credits] Abin Krishna, Kishen PC, Vaishak")
print("="*80+"""

  ____             _    _        ____                      
 |  _ \ ___   ___ | | _(_) ___  | __ )  ___  __ _ _ __ ____
 | |_) / _ \ / _ \| |/ / |/ _ \ |  _ \ / _ \/ _` | '__|_  /
 |  __/ (_) | (_) |   <| |  __/ | |_) |  __/ (_| | |   / / 
 |_|   \___/ \___/|_|\_\_|\___| |____/ \___|\__,_|_|  /___|
                                                           
""")


try:
    print("\n\t\t\tEnter SQL Server Connection Details\n")
    print("_"*91)

    host = input("\n(Hostname) > ")
    user = input("(Username) > ")
    db = input("(Database Name) > ")
    passwd = getpass("(Database Connection Password) > ")
    # By using "getpass" whenever u type the password it will be hidden in the terminal
    
    conn = sq.connect(host=host, username=user , database=db, passwd=passwd)
    
    if conn.is_connected():
        print(f"\n[⁎] Connected to {host}")
        print(f"[⁎] Welcome To The {db} Databse Interface\n")
        print("[⁎] List of Tables-")
        show_tables()
        print("\n")

        while conn.is_connected():
            print("""Database Queries:-
            1. Describe a Table
            2. Insert A Value
            3. Close Connection
            4. Select Data""")

            action = input("(Enter Command) > ")
            if action in ["Close Connection", "CLOSE CONNECTION", "3"]:
                conn.close()
            if action in ["Describe a Table", "DESCRIBE A TABLE", "1"]:
                describe_table()  
            if action in ["Insert A Value", "INSERT A VALUE", "2"]:
                insert_values()
            if action in ["Select Data", "SELECT DATA", "4"]:
                pass

except sq.Error:
    print("\n[!] Connection Failed!")
    print("[!] Make sure you have entered the right credentials for the database connection\n")

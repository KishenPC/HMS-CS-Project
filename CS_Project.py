# Imports
import mysql.connector as sq
from getpass import getpass

# [!] - for errors
# [⁎] - for goods (i dont know what to write here)
# [#] - if something is not available or not found or if nothing is changed
# [&] - for showing info

# Functions
def describe_table():
    cursor = conn.cursor()
    table = input("(HMS: Enter Name Of Table To Describe) > ")
    cursor.execute(f"DESCRIBE {table}")
    table_desc = cursor.fetchall()
    columns = {} 
    print("\n[⁎] The Format Is, {Column Name : Data Type}")
    for i in table_desc:
        columns.update({i[0]:i[1].upper()})
    print(f"    {columns}\n")

def all_tables():
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
        print("\t•———————————————————•")
        print("\tList of Tables\n")
        for i in tables:
            print(f"\t{tables.index(i)+1}| {i}")
        print("\t•———————————————————•")

def insert_values():
    cursor = conn.cursor()
    table = input("(HMS: Enter Table Name) > ")
    entries = int(input("(HMS: Enter Number Of Entries) > "))

    print("[⁎] The Columns Of The Table is as Follows: ")
    cursor.execute(f"DESCRIBE {table}")
    table_desc = cursor.fetchall()
    columns = {} 
    for i in table_desc:
        columns.update({i[0]:i[1].upper()})
    print(f"    {columns}")

    ent=[]
    print("[&] If you don't have a value type null")
    for i in range(entries):
        entry = tuple(input("(HMS: Enter values) > ").split())
        if not entry:
            print("[!] No value is entered")
            break
        else:
            ent.append(entry)

    cursor.executemany("INSERT INTO "+table+" VALUES(%s, %s, %s, %s, %s, %s)", ent)
    # replacing null with NULL (this is the only way i could find)
    cursor.execute(f"""UPDATE {table}
                SET Name=NULL
                WHERE Name='null'""")
    cursor.execute(f"""UPDATE {table}
                   SET Age=NULL
                   WHERE Age='null'""")
    cursor.execute(f"""UPDATE {table}
                   SET Place=NULL
                   WHERE Place='null'""")
    cursor.execute(f"""UPDATE {table}
                   SET a=NULL
                   WHERE a='null'""")
    cursor.execute(f"""UPDATE {table}
                   SET b=NULL
                   WHERE b='null'""")
    cursor.execute(f"""UPDATE {table}
                   SET c=NULL
                   WHERE c='null'""")
    commit=input("(Do you want to commit changes?) Y/n > ")
    if commit in ["y", "Y"] or commit.upper()=="YES":
        print("\n[+] New values got added into the database\n")
        conn.commit()
    elif commit in ["n", "N"] or commit.upper()=="NO":
        print("\n[#] No changes took place\n")
    else:
        print("\n[!] Error: Wrong input\n")
    # '%s' is the no. of columns (you can change it according to the no. of columns)

# this display table looks shit (it is not even a table but i will try to change it)
def show_table():
    d_table = input("(HMS: Enter Table Name) > ")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM "+d_table)
    item=cursor.fetchall()
    for i in item:
        print(i)

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
        
        conn.commit()

# Code
print("\n"+"="*81)
print("  [Project] Hospital Management System")
print("="*81)

print("  [Credits] Abin Krishna, Kishen PC, Vaishak")
print("="*81+"""

  ____             _    _        ____                      
 |  _ \ ___   ___ | | _(_) ___  | __ )  ___  __ _ _ __ ____
 | |_) / _ \ / _ \| |/ / |/ _ \ |  _ \ / _ \/ _` | '__|_  /
 |  __/ (_) | (_) |   <| |  __/ | |_) |  __/ (_| | |   / / 
 |_|   \___/ \___/|_|\_\_|\___| |____/ \___|\__,_|_|  /___|
                                                           
""")


try:
    print("\n\t\t\tEnter SQL Server Connection Details\n")
    print("—"*81)

    host = input("\n(Bearz: Hostname) > ")
    user = input("(Bearz: Username) > ")
    db = input("(Bearz: Database Name) > ")
    passwd = getpass("(Bearz: Database Connection Password) > ")
    # By using "getpass" whenever u type the password it will be hidden in the terminal
    
    conn = sq.connect(host="localhost", username="root" , database="customers", passwd="Server###Beast69#")
    
    if conn.is_connected():
        print(f"\n[⁎] Connected to {host}")
        print(f"[⁎] Welcome To The {db} Databse Interface\n")
        print("List of Tables:-")
        all_tables()

        while conn.is_connected():
            print("""\nDatabase Queries:-
\t1. Describe a Table
\t2. Select Data
\t3. Insert A Value
\t4. Show table
\t5. Close Connection\n""")

            action = input("(HMS: Enter Command) > ")
            if action.upper()=="DESCRIBE A TABLE" or action=="1":
                describe_table()
            if action.upper()=="SELECT DATA" or action=="2":
                pass
            if action.upper()=="INSERT A VALUE" or action=="3":
                insert_values()
            if action.upper()=="SHOW TABLE" or action=="4":
                show_table()
            if action.upper()=="CLOSE CONNECTION" or action=="5":
                con_quit=input("Do you want to exit (close connection) ? press 'q' to exit: ")
                if con_quit.upper()==["QUIT"] or con_quit in ["q", "Q"]:
                    conn.close()
                    print()
            if action.upper()=="EXIT":
                conn.close()
                print()
            else:
                print("[!] Error: Wrong input")

except sq.Error:
    print("\n[!] Error: Connection Failed!")
    print("[!] Error: Make sure you have entered the right credentials for the database connection\n")

# this KeyboardInterrupt error happens when u press ctrl+c
except KeyboardInterrupt:
    ki_error=input("Do you want to exit ? press any letter to exit: ")
    exit
    print()

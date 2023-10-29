# Imports
import mysql.connector as sq
from getpass import getpass
import os

# [!] - for errors
# [⁎] - for goods (i dont know what to write here)
# [#] - if something is not available or not found or if nothing is changed
# [+] - if something new is added
# [&] - for showing info
# [$] - for showing warning

# Function of HMS
def create_tables():
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE Doctor(
        Doctor_ID INT PRIMARY KEY AUTO_INCREMENT,
        First_Name VARCHAR(15),
        Last_Name VARCHAR(15),
        Specialization VARCHAR(30),
        Doctor_Age INT,
        Doctor_Gender VARCHAR(6),
        Address VARCHAR(50),
        Phone VARCHAR(11))""")

    cursor.execute("""CREATE TABLE Patient(
        Patient_ID INT PRIMARY KEY AUTO_INCREMENT,
        Under_Treatment_of VARCHAR(40),
        First_Name VARCHAR(15),
        Last_Name VARCHAR(15),
        Patient_Age INT,
        Date_of_Birth DATE,
        Patient_Gender VARCHAR(6),
        Address VARCHAR(50),
        Phone VARCHAR(11),
        Insurance_ID INT,
        Admission_Date DATE)""")
    
    cursor.execute("""CREATE TABLE Diagnosis(
        Patient_ID INT PRIMARY KEY AUTO_INCREMENT,
        Patient_Diagnosis VARCHAR(100),
        Room_Number INT)""")

def drop_tables():
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    listed_tables = cursor.fetchall()
    tables = []
    for i in listed_tables: #Due to the fact that returned list of tables in the form [(t1,),(t2,)]
        for z in i:
            tables.append(z)
        print(z)
    print(i)
    drop_table = f"DROP TABLE {tables[0]}"

    if len(tables) == 1:
        cursor.execute(drop_table)
    else:
        for i in tables[1:]:
            drop_table += f", {i}"
        cursor.execute(drop_table)
    conn.commit()

def hosptial_db_setup():
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    show_tables = cursor.fetchall()
    tables = []

    for i in show_tables:
        for z in i: #Due to the fact that returned list of tables in the form [(t1,),(t2,)]
            tables.append(z)

    if 'patient' in tables and 'doctor' in tables and "diagnosis" in tables:
        print()

    elif 'patient' not in tables and 'doctor' not in tables and "diagnosis" not in tables:
        create_tables()
        conn.commit()

    else:
        print("\n[!] Error: Found Incomplete Database")
        reset = input("(Reset Database?) y/N > ")
        if reset.upper() == "YES" or reset==['y', 'Y']:
            drop_tables()
            create_tables()

        elif reset.upper() == "NO" or reset==['n', 'N']:
            print("\n[#] Please Swap to a Different Database")
            conn.close()

# Functions
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

def describe_table():
    cursor = conn.cursor()
    table = input("(HMS: Enter Table Name To Describe (patient, doctor, diagnosis)) > ")
    cursor.execute(f"DESCRIBE {table}")
    table_desc = cursor.fetchall()
    columns = {} 
    print("\n[&] The Format Is, {Column Name : Data Type}")
    for i in table_desc:
        columns.update({i[0]:i[1].upper()})
    print(f"    {columns}\n")

def insert_values():
    cursor = conn.cursor()
    table = input("(HMS: Enter Table Name (patient, doctor, diagnosis)) > ")
    entries = int(input("(HMS: Enter Number Of Entries) > "))

    print("[&] The Columns Of The Table is as Follows: ")
    cursor.execute(f"DESCRIBE {table}")
    table_desc = cursor.fetchall()
    columns = {} 
    for i in table_desc:
        columns.update({i[0]:i[1].upper()})
    print(f"    {columns}")

    ent=[]
    print("\n[&] If you don't have a value, type 'null' (Except: DoB, Age, Insurance ID, Admission Date)")
    print("[&] The format for writing date is (dd,mm,yyyy)\n")
    for j in range(entries):
        entry = tuple(input("(HMS: Enter values) > ").split())
        if not entry:
            print("[!] Error: No value is entered")
            break
        else:
            ent.append(entry)
            e=list(entry)
            if table.upper() == "PATIENT":
                e[3]=int(e[3])
                e[8]=int(e[8])

                # this is for inserting date(i dont know if there is any other way of it)
                c=e[4]
                d=c[0]+c[1]
                d=int(d)
                m=c[3]+c[4]
                m=int(m)
                y=c[6]+c[7]+c[8]+c[9]
                y=int(y)
                a=sq.Date(y, m, d)
                e.remove(e[4])
                e.insert(4, a)

                k=e[9]
                day=k[0]+k[1]
                day=int(day)
                month=k[3]+k[4]
                month=int(month)
                year=k[6]+k[7]+k[8]+k[9]
                year=int(year)
                b=sq.Date(year, month, day)
                e.remove(e[9])
                e.insert(9, b)
                
                e=tuple(e)
                n_ent=[]
                n_ent.append(e)
                print(n_ent)

                cursor.executemany("""INSERT INTO patient(Under_Treatment_of, First_Name, Last_Name,
                              Patient_Age, Date_of_Birth, Patient_Gender,
                               Address, Phone, Insurance_ID,
                               Admission_Date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", n_ent)
                
                cursor.execute("""UPDATE patient
                                SET Under_Treatment_of=NULL
                                WHERE Under_Treatment_of='null'""")
                cursor.execute("""UPDATE patient
                                SET First_Name=NULL
                                WHERE First_Name='null'""")
                cursor.execute("""UPDATE patient
                                SET Last_Name=NULL
                                WHERE Last_Name='null'""")
                cursor.execute("""UPDATE patient
                                SET Patient_Gender=NULL
                                WHERE Patient_Gender='null'""")
                cursor.execute("""UPDATE patient
                                SET Address=NULL
                                WHERE Address='null'""")
                cursor.execute("""UPDATE patient
                                SET Phone=NULL
                                WHERE Phone='null'""")
            else:
                print("[!] Error: Wrong Table Name")
    # '%s' is the no. of columns (you can change it according to the no. of columns)

    commit=input("(Do you want to commit changes?) Y/n > ")
    if commit in ["y", "Y"] or commit.upper()=="YES":
        print("\n[+] New values got added into the database")
        conn.commit()
    elif commit in ["n", "N"] or commit.upper()=="NO":
        print("\n[#] No changes took place")
    else:
        print("\n[!] Error: Wrong input")

def reset_db():
    cursor=conn.cursor()
    cursor.execute("DELETE FROM Patient")
    cursor.execute("DELETE FROM Doctor")
    cursor.execute("DELETE FROM Diagnosis")
    
    print("\n[$] This will result in loss of all data present in the Database Tables\n")
    reset=input("(Do you want to commit changes?) Y/n > ")
    if reset in ["y", "Y"] or reset.upper()=="YES":
        print("\n[+] Database Tables got cleared")
        conn.commit()
    elif reset in ["n", "N"] or reset.upper()=="NO":
        print("\n[#] No changes took place")
    else:
        print("\n[!] Error: Wrong input")

# this display table looks shit (it is not even a table but i will try to change it)
def show_table():
    d_table = input("(HMS: Enter Table Name) > ")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM "+d_table)
    item=cursor.fetchall()
    if len(item)==0:
        print("[#] No values availabe (empty table)")
    else:
        for i in item:
            print(i)

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
    print("\n\t\t       Enter SQL Server Connection Details\n")
    print("—"*81)

    host = input("\n(Bearz: Hostname) > ")
    user = input("(Bearz: Username) > ")
    db = input("(Bearz: Database Name) > ")
    passwd = getpass("(Bearz: Database Connection Password) > ")
    # By using "getpass" whenever u type the password it will be hidden in the terminal
    
    conn = sq.connect(host=host, username=user , database=db, passwd=passwd)
    
    if conn.is_connected():
        print(f"\n[⁎] Connected to {host}")
        print(f"[⁎] Welcome To The {db} Databse Interface\n")
        print("List of Tables:-")
        hosptial_db_setup()
        all_tables()

        while conn.is_connected():
            print("""\nDatabase Queries:-
\t1. Describe Table
\t2. Select Data
\t3. Insert Value(s)
\t4. Show table
\t5. Reset Database
\t6. Close Connection\n""")

            action = input("(HMS: Enter Command) > ")
            if action.upper()=="DESCRIBE A TABLE" or action=="1":
                describe_table()
            elif action.upper()=="SELECT DATA" or action=="2":
                pass
            elif action.upper()=="INSERT A VALUE" or action=="3":
                insert_values()
            elif action.upper()=="SHOW TABLE" or action=="4":
                show_table()
            elif action.upper()=="RESET DATABASE" or action=="5":
                reset_db()
            elif action.upper()=="CLOSE CONNECTION" or action=="6":
                con_quit=input("Do you want to exit (close connection) ? press 'q' to exit: ")
                if con_quit.upper()==["QUIT"] or con_quit in ["q", "Q"]:
                    conn.close()
                    print()
                else:
                    print("Type 'q' to exit")
            
            # Hidden Commands 💀
            elif action.upper()=="HELP" or action=="?":
                print("\nMain Commands")
                print("¯¯¯¯¯¯¯¯¯¯¯¯¯")
                print("\n\tCommands\tDescription")
                print("\t¯¯¯¯¯¯¯¯\t¯¯¯¯¯¯¯¯¯¯¯")
                print("\thelp\t\tHelp menu")
                print("\t?\t\talias for help")
                print("\tclear\t\tClears the screen")
                print("\texit\t\tExit the console")
            elif action.upper()=="CLEAR":
                os.system("cls")
            elif action.upper()=="EXIT":
                conn.close()
                print()
            
            else:
                print("[!] Error: Wrong input")

except sq.Error:
    print("\n[!] Error: Connection Failed!")
    print("[!] Error: Make sure you have entered the right credentials for the database connection\n")

# this KeyboardInterrupt error happens when u press ctrl+c
except KeyboardInterrupt:
    ki_error=input("Do you want to exit ? press 'Enter' to exit: ")
    exit
    print()

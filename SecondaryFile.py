# START

# Imports
import mysql.connector as sq
from getpass import getpass
from tabulate import tabulate
from datetime import datetime
import msvcrt
import time
import os

# [!] - for errors
# [⁎] - for goods (i dont know what to write here)
# [#] - if something is not available or not found or if nothing is changed
# [+] - if something new is added
# [&] - for showing info
# [$] - for showing warning
# [—] - for Unknown Command

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
        Patient_Diagnosis VARCHAR(40),
        Room_Number INT,
        Treated_By VARCHAR(30))""")

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
        reset = input("(Reset Database?) y/n > ")
        if reset.upper() in ["YES","Y"]:
            drop_tables()
            create_tables()

        elif reset.upper() in ["NO","N"]:
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
    table = input("(HMS: Enter Table Name (patient, doctor)) > ")
    entries = int(input("(HMS: Enter Number Of Entries) > "))

    print("\n[&] The Columns Of The Table is as Follows: ")
    cursor.execute(f"DESCRIBE {table}")
    table_desc = cursor.fetchall()
    columns = {} 
    for i in table_desc:
        if i != table_desc[0]: #Excluding Entry of ID Of Main Tables To Implement AUTO_INCREMENT
            columns.update({i[0]:i[1].upper()})
    print(f"    {columns}")

    print("\n[&] After every value put a '/' (Example: abcd/efgh/123)")
    print("[&] If you don't have a value, Leave Empty (Example: abc/def//123)")
    print("[&] The format for writing date is (yyyy-mm-dd)\n")
    for j in range(entries):
        entry = tuple(input("(HMS: Enter values) > ").split("/"))
        
        if not entry:
            print("[!] Error: No value is entered")
            break
        else:
            if table.upper() == "PATIENT":
                e=list(entry) #Forms a List Of Entered Values

                DoBFormat = list(map(int,e[3].split("-")))
                DoB = datetime.date(DoBFormat[0],DoBFormat[1],DoBFormat[2]) #Date Of Birth Formatting (To Understand Better, Print DOBFormat)

                DoAFormat = list(map(int,e[8].split("-")))
                DoA = datetime.date(DoAFormat[0],DoAFormat[1],DoAFormat[2]) #Date Of Admission Formatting ( To Understand Better, Print DOAFormat)

                data = e[0:3] + [DoB,] + e[4:8] + [DoA,] #Combinaton of Values And Dates Into One List
                cursor.execute("""INSERT INTO patient
                (First_Name, Last_Name, Patient_Age, Date_of_Birth, 
                Patient_Gender, Address, Phone, Insurance_ID, Admission_Date) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",data) #For 9 Columned Row Of Inputs

                # This is required (Because when we dont have a value it enteres nothing in the db cell, it should enter NULL)
                cursor.execute("""UPDATE patient
                            SET First_Name=NULL
                            WHERE First_Name=''""")
                cursor.execute("""UPDATE patient
                            SET Last_Name=NULL
                            WHERE Last_Name=''""")
                cursor.execute("""UPDATE patient
                            SET Patient_Age=NULL
                            WHERE Patient_Age=''""")
                cursor.execute("""UPDATE patient
                            SET Patient_Gender=NULL
                            WHERE Patient_Gender=''""")
                cursor.execute("""UPDATE patient
                            SET Address=NULL
                            WHERE Address=''""")
                cursor.execute("""UPDATE patient
                            SET Phone=NULL
                            WHERE Phone=''""")
                cursor.execute("""UPDATE patient
                            SET Insurance_ID=NULL
                            WHERE Insurance_ID=''""")

                patient_diagnosis = input("(HMS: Patient diagnosed with) > ")
                print("\n[&] If there is no room number, type 0\n")
                patient_room = int(input("(HMS: Patient Room (If Any)) > "))
                treated_by = input("\n(HMS: Treated By) > ")
                    
                if patient_room != 0:
                    cursor.execute(f"INSERT INTO diagnosis(Patient_Diagnosis, Room_Number, Treated_By) VALUES {patient_diagnosis, patient_room, treated_by}")
                    cursor.execute("""UPDATE diagnosis
                            SET Patient_Diagnosis=NULL
                            WHERE Patient_Diagnosis=''""")
                    cursor.execute("""UPDATE diagnosis
                            SET Treated_By=NULL
                            WHERE Treated_By=''""")

                elif patient_room == 0:
                    data = (patient_diagnosis, None, treated_by)
                    cursor.execute(f"INSERT INTO diagnosis(Patient_Diagnosis, Room_Number, Treated_By) VALUES (%s, %s, %s)", data)

            elif table.upper() == "DOCTOR":
                data=list(entry)
                cursor.execute("""INSERT INTO doctor
                (First_Name, Last_Name, Specialization,
                Doctor_Age, Doctor_Gender, Address, Phone)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",data)

    commit=input("(Do you want to commit changes?) Y/n > ")
    if commit.upper() in ["YES", "Y"]:
        print("\n[+] New values got added into the database")
        conn.commit()
    elif commit.upper() in ["NO", "N"]:
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
    if reset.upper() in ["YES", "Y"]:
        print("\n[+] Database Tables got cleared")
        conn.commit()
    elif reset.upper() in ["NO", "N"]:
        print("\n[#] No changes took place")
    else:
        print("\n[!] Error: Wrong input")

def show_table():
    s_table = input("(HMS: Enter Table Name (patient, doctor, diagnosis)) > ")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM "+s_table)
    item=cursor.fetchall()
    if len(item)==0:
        print("\n[#] No values availabe (empty table)")
    else:
        """for i in item:
            print(i)"""
        fmt="double_grid"
        if s_table.upper()=="PATIENT":
            p_header=["Patient ID", "First Name", "Last Name", "Patient Age", "DoB", "Gender", "Address", "Phone", "Insurance ID", "Admission Date"]
            print(tabulate(item, headers=p_header, tablefmt=fmt))
        elif s_table.upper()=="DOCTOR":
            doc_header=["Doctor ID", "First Name", "Last Name", "Specialization", "Age", "Gender", "Address", "Phone"]
            print(tabulate(item, headers=doc_header, tablefmt=fmt))
        elif s_table.upper()=="DIAGNOSIS":
            diag_header=["Patient ID", "Patient Diagnosis", "Room Number"]
            print(tabulate(item, headers=diag_header, tablefmt=fmt))
        else:
            print("[!] Error: Wrong Table Name")

# Code
print("\n"+"="*81)
print("  [Project] Hospital Management System")
print("="*81)

print("  [Credits] Abin Krishna, Kishen PC, Vaishak")
print("="*81+"""
            
                       ██╗  ██╗    ███╗   ███╗    ███████╗
                       ██║  ██║    ████╗ ████║    ██╔════╝
                       ███████║    ██╔████╔██║    ███████╗
                       ██╔══██║    ██║╚██╔╝██║    ╚════██║
                       ██║  ██║    ██║ ╚═╝ ██║    ███████║
                       ╚═╝  ╚═╝    ╚═╝     ╚═╝    ╚══════╝
""")

try:
    print("\n\t\t       Enter SQL Server Connection Details\n")
    print("—"*81)

    host = input("\n(HMS: Hostname) > ")
    user = input("(HMS: Username) > ")
    db = input("(HMS: Database Name) > ")
    passwd = getpass("(HMS: Database Connection Password) > ")
    # By using "getpass" whenever u type the password it will be hidden in the terminal
    
    conn = sq.connect(host=host, username=user , database=db, passwd=passwd)
    
    if conn.is_connected():
        print("\nStarting the Hospital Management System Console.../")
        time.sleep(1.5)
        print(f"\n[⁎] Connected to {host}")
        print(f"[⁎] Welcome To The {db} Databse Interface\n")
        print("List of Tables:-")
        hosptial_db_setup()
        all_tables()

        while conn.is_connected():
            print("""\nDatabase Commands:-
\t1. Describe Table
\t2. Select Data
\t3. Insert Value(s)
\t4. Remove Value(s)
\t5. Show Table
\t6. Reset Database
\t7. Disconnect\n""")

            action = input("(HMS: Enter Command) > ")
            if action.upper() in ("DESCRIBE TABLE", "1"):
                describe_table()
            elif action.upper() in ("SELECT DATA", "SELECT", "2"):
                pass
            elif action.upper() in ("INSERT VALUES", "INSERT VALUE", "INSERT", "3"):
                insert_values()
            elif action.upper() in ("REMOVE VALUES", "REMOVE VALUE", "REMOVE", "4"):
                remove_values()
            elif action.upper() in ("SHOW TABLE", "5"):
                show_table()
            elif action.upper() in ("RESET DATABASE", "RESET", "6"):
                reset_db()
            elif action.upper() in ("DISCONNECT", "7"):
                con_quit=input("Do you wish to Disconnect? Enter 'q' to exit: ")
                if con_quit.upper() in ["QUIT", "Q"]:
                    conn.close()
                    print()
                else:
                    print("Type 'q' to exit")

            # Hidden Commands 💀
            elif action.upper() in ["HELP", "?"]:
                print("\n Main Commands")
                print("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
                print("\n\t Commands\t Description")
                print("\t¯¯¯¯¯¯¯¯¯¯\t¯¯¯¯¯¯¯¯¯¯¯¯¯")
                print("\thelp\t\tHelp menu")
                print("\tbanner\t\tDisplays a banner")
                print("\t?\t\talias for help")
                print("\tclear\t\tClears the screen")
                print("""\tcolor\t\tChanges the color of the terminal\n
                        1 = Aqua        2 = Purple
                        3 = Blue        4 = Green
                        5 = White""")
                print("\n\texit\t\tExit the console")
            elif action.upper() == "BANNER":
                print("""

██╗  ██╗    ███╗   ███╗    ███████╗
██║  ██║    ████╗ ████║    ██╔════╝
███████║    ██╔████╔██║    ███████╗
██╔══██║    ██║╚██╔╝██║    ╚════██║
██║  ██║    ██║ ╚═╝ ██║    ███████║
╚═╝  ╚═╝    ╚═╝     ╚═╝    ╚══════╝
                                                                             
""")
            elif action.upper()=="CLEAR":
                os.system("cls")
            elif action.upper()=="EXIT":
                conn.close()
                print()

            # Terminal Color (BTW it looks so good)
            elif action.upper()=="COLOR 1":
                os.system("color 3")
            elif action.upper()=="COLOR 2":
                os.system("color 5")
            elif action.upper()=="COLOR 3":
                os.system("color 1")
            elif action.upper()=="COLOR 4":
                os.system("color 2")
            elif action.upper()=="COLOR 5":
                os.system("color 7")
            
            else:
                print("[—] Unknown command")

# This works only if the credentials are wrong
except sq.Error as err:
    if err.errno==sq.errorcode.ER_ACCESS_DENIED_ERROR:
        print("\n[!] Access Denied")
        print("[!] Make sure you have entered the right credentials for the database connection\n")
    else:
        print("[!] There was an Error")

# this KeyboardInterrupt error happens when u press ctrl+c
except KeyboardInterrupt:
    print("Press any key to exit...")
    # ↓ this line of code takes any keystroke
    msvcrt.getch()
    exit
    print()

# END

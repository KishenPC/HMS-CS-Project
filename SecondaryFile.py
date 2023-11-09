# START

# Imports
import mysql.connector as sq
import datetime
import os
from tabulate import tabulate # pip install tabulate

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
        if reset.upper() in ["YES", "Y"]:
            drop_tables()
            create_tables()

        elif reset.upper() in ["NO", "N"]:
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
    try:    
        cursor.execute(f"DESCRIBE {table}")
        table_desc = cursor.fetchall()
        columns = {} 
        print("\n[&] The Format Is, {Column Name : Data Type}")
        for i in table_desc:
            columns.update({i[0]:i[1].upper()})
        print(f"    {columns}\n")
    except:
        print("\n[!] Error: Table Doesn't Exist")

def insert_values():
    cursor = conn.cursor()
    table = input("(HMS: Enter Table Name (patient, doctor)) > ")
    entries = int(input("(HMS: Enter Number Of Entries) > "))

    print("[&] The Columns Of The Table is as Follows: ")
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
                    
                patient_diagnosis = input("(HMS: Patient Diagnosis) > ")
                print("\n[&] If there is no room number, type 0")
                patient_room = int(input("(HMS: Patient Room (If Any)) > "))
                treated_by = input("(HMS: Treated By) > ")

                data = e[0:3] + [DoB,] + e[4:8] + [DoA,] #Combinaton of Values And Dates Into One List
                cursor.execute("""INSERT INTO patient
                (First_Name, Last_Name, Patient_Age, Date_of_Birth, 
                Patient_Gender,Address, Phone, Insurance_ID, Admission_Date) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",data) #For 9 Columned Row Of Inputs
                     
                if patient_room != 0:
                    cursor.execute(f"INSERT INTO diagnosis(Patient_Diagnosis, Room_Number, Treated_By) VALUES {patient_diagnosis, patient_room, treated_by}")
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
    if commit in ["YES", "Y"]:
        print("\n[+] New values got added into the database")
        conn.commit()
    elif commit.upper() in ["NO", "N"]:
        print("\n[#] No changes took place")
    else:
        print("\n[!] Error: Wrong input")

def reset_db():
    conn_cursor = conn.cursor()
    print("\n[$] This will result in loss of all data present in the Database Tables")
    reset = input("Proceed With Reset? (y/n) > ")
    if reset.upper() in ("YES","Y"):
        #
        drop_tables()
        create_tables()
        #
        print("\n[+] Successful Database Reset ")
        all_tables()
        
    elif reset.upper() in ("NO","N"):
        print("\n[#] Database Reset Cancelled")

    else:
        print("\n[!] Error: Wrong input")

# this display table looks shit (it is not even a table but i will try to change it)
def show_table():
    s_table = input("(HMS: Enter Table Name (patient, doctor, diagnosis)) > ")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM "+s_table)
    item=cursor.fetchall()
    if len(item) == 0:
        print("[#] No values availabe (empty table)")
    else:
        """for i in item:
            print(i)"""
        if s_table.upper()=="PATIENT":
            p_header=["Patient ID", "First Name", "Last Name", "Age", "Date Of Birth", "Sex", "Address", "Phone", "Insurance ID", "Date Of Admission"]
            print(tabulate(item, headers=p_header, tablefmt="double_grid"))
        elif s_table.upper()=="DOCTOR":
            d_header=["Doctor ID", "First Name", "Last Name", "Specialization", "Age", "Sex", "Address", "Phone"]
            print(tabulate(item, headers=d_header, tablefmt="double_grid"))
        if s_table.upper()=="DIAGNOSIS":
            diag_header=["Patient ID", "Diagnosis", "Room Number", "Treated By"]
            print(tabulate(item, headers=diag_header, tablefmt="double_grid"))
        else:
            print("[!] Error: Wrong Table Name")

# Code
print("\n"+"="*81)
print("  [Project] Hospital Management System")
print("="*81)

print("  [Credits] Abin Krishna, Kishen PC, Vaishak")
print("="*81)

try:
    print("\n\t\t       Enter SQL Server Connection Details\n")
    print("—"*81)

    host = input("\n(HMS: Hostname) > ")
    user = input("(HMS: Username) > ")
    db = input("(HMS: Database Name) > ")
    passwd = input("(HMS: Database Connection Password) > ")
    
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
\t6. Disconnect\n""")

            action = input("(HMS: Enter Command) > ")
            if action.upper() in ("DESCRIBE TABLE", "1"):
                describe_table()
            elif action.upper() in ("SELECT DATA", "SELECT", "2"):
                pass
            elif action.upper() in ("INSERT VALUES", "INSERT", "3"):
                insert_values()
            elif action.upper() in ("SHOW TABLE", "4"):
                show_table()
            elif action.upper() in ("RESET DATABASE", "RESET", "5"):
                reset_db()
            elif action.upper() in ("DISCONNECT", "6"):
                con_quit=input("Do you want to exit (close connection) ? press 'q' to exit: ")
                if con_quit.upper()==["QUIT"] or con_quit in ["q", "Q"]:
                    conn.close()
                    print()
                else:
                    print("Type 'q' to exit")
            
            # Hidden Commands 💀
            elif action.upper() in ("HELP", "?"):
                print("\nMain Commands")
                print("¯¯¯¯¯¯¯¯¯¯¯¯¯")
                print("\n\tCommands\tDescription")
                print("\t¯¯¯¯¯¯¯¯\t¯¯¯¯¯¯¯¯¯¯¯")
                print("\thelp\t\tHelp menu")
                print("\tbanner\t\tDisplays a banner")
                print("\t?\t\talias for help")
                print("\tclear\t\tClears the screen")
                print("\texit\t\tExit the console")
            elif action.upper() in ("CLEAR"):
                os.system("cls")
            elif action.upper() in ("EXIT"):
                conn.close()
                print()
            
            else:
                print("[!] Error: Wrong input")

except sq.Error:
    print("\n[!] Error: Connection Failed!")
    print("[!] Error: Make sure you have entered the right credentials for the database connection\n")

# this KeyboardInterrupt error happens when u press ctrl+c
except KeyboardInterrupt:
    ki_error=input("Do you want to exit ? press 'Enter' or any key to exit: ")
    exit
    print()

# END

# START

# Imports
import mysql.connector as sq
from getpass import getpass
from tabulate import tabulate
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
    curs = conn.cursor()

    curs.execute("""CREATE TABLE Doctor(
        Doctor_ID INT PRIMARY KEY AUTO_INCREMENT,
        First_Name VARCHAR(15),
        Last_Name VARCHAR(15),
        Specialization VARCHAR(30),
        Age INT,
        Sex VARCHAR(6),
        Address VARCHAR(50),
        Phone VARCHAR(11))""")

    curs.execute("""CREATE TABLE Patient(
        Patient_ID INT PRIMARY KEY AUTO_INCREMENT,
        First_Name VARCHAR(15),
        Last_Name VARCHAR(15),
        Age INT,
        Date_of_Birth DATE,
        Sex VARCHAR(6),
        Address VARCHAR(50),
        Phone VARCHAR(11),
        Insurance_ID INT,
        Date_Of_Admission DATE)""")
    
    curs.execute("""CREATE TABLE Diagnosis(
        Patient_ID INT PRIMARY KEY AUTO_INCREMENT,
        Patient_Diagnosis VARCHAR(40),
        Room_Number INT,
        Treated_By VARCHAR(30))""")

def drop_tables():
    curs = conn.cursor()
    curs.execute("SHOW TABLES")
    listed_tables = curs.fetchall()
    tables = []
    for i in listed_tables: #Due to the fact that returned list of tables in the form [(t1,),(t2,)]
        for z in i:
            tables.append(z)
        print(z)
    print(i)
    drop_table = f"DROP TABLE {tables[0]}"

    if len(tables) == 1:
        curs.execute(drop_table)
    else:
        for i in tables[1:]:
            drop_table += f", {i}"
        curs.execute(drop_table)
    conn.commit()

def hosptial_db_setup():
    curs = conn.cursor()
    curs.execute("SHOW TABLES")
    show_tables = curs.fetchall()
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
        if reset.upper() in ["YES", 'Y']:
            drop_tables()
            create_tables()

        elif reset.upper() in ["NO", 'N']:
            print("\n[#] Please Swap to a Different Database")
            conn.close()

# Functions
def all_tables():
    curs = conn.cursor()
    curs.execute("SHOW TABLES")
    show_tables = curs.fetchall()
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
    curs = conn.cursor()
    table = input("(HMS: Enter Table Name To Describe (patient, doctor, diagnosis)) > ")
    if table.upper() in ["PATIENT", "DOCTOR", "DIAGNOSIS"]:
        curs.execute(f"DESCRIBE {table}")
        table_desc = curs.fetchall()
        columns = {} 
        print("\n[&] The Format Is, {Column Name : Data Type}")
        for i in table_desc:
            columns.update({i[0]:i[1].upper()})
        print(f"    {columns}\n")
    else:
        print("\n[!] Error: Wrong Table Name")

def select_data():
    # I made the header as an item of the table and remove the header from tabulate so it will look like column names only
    curs=conn.cursor()
    table = input("(HMS: Enter Table Name (patient, doctor, diagnosis)) > ")
    if table.upper() in ["PATIENT", "DOCTOR", "DIAGNOSIS"]:
        curs.execute("SELECT * FROM "+table)
        item=curs.fetchall()
        fmt="double_grid"
        
        if table.upper()=="PATIENT":
            p_header=["Patient_ID", "First_Name", "Last_Name", "Age", "Date_Of_Birth", "Sex", "Address", "Phone", "Insurance ID", "Date_Of_Admission"]
            print()
            print(tabulate([p_header], tablefmt=fmt))
            print()
        
        elif table.upper()=="DOCTOR":
            doc_header=["Doctor_ID", "First_Name", "Last_Name", "Specialization", "Age", "Sex", "Address", "Phone"]
            print()
            print(tabulate([doc_header], tablefmt=fmt))
            print()
        
        elif table.upper()=="DIAGNOSIS":
            diag_header=["Patient_ID", "Diagnosis", "Room_Number"]
            print()
            print(tabulate([diag_header], tablefmt=fmt))
            print()
        
        if len(item)==0:
            print("[#] No values availabe (empty table)\n")
        
        elif len(item) != 0:
            column_count = input("(HMS: Columns to Display (Selective/All)) > ")
            if column_count.upper() == "SELECTIVE":
                try:
                    columns = input("(HMS: Enter The Name Of The Columns Seperated By Comma) > ")
                    try:
                        condition_count = int(input("(HMS: Number Of Conditions) > "))
                        
                        if condition_count == 0:
                            curs.execute(f"SELECT {columns} FROM {table}")
                            selected = curs.fetchall()
                            print()
                            p_header=[x for x in columns.split(",")]
                            print(p_header)
                            print(tabulate(selected, headers=p_header, tablefmt=fmt))
                            print()
                        
                        elif condition_count > 0:
                            conditions = ""
                            
                            for i in range(condition_count):
                                condition_column = input(f"(HMS: Enter Column To Use As Condition {i+1}) > ")
                                condition_value = input(f"(HMS: Enter Value To Search With Respect To Column Condition {i+1}) > ")
                                
                                if not condition_value.isdigit():
                                    condition_value = f"'{condition_value}'"
                                conditions += f"{condition_column} = {condition_value}"
                                
                                if condition_count == 1:
                                    pass
                                elif i == (condition_count - 1):
                                    pass
                                else:
                                    conditions += " AND "
                            
                            print("\n"+f"SELECT {columns} FROM {table} WHERE {conditions}")
                            curs.execute(f"SELECT {columns} FROM {table} WHERE {conditions}")
                            selected = curs.fetchall()
                            p_header=[x for x in columns.split(",")]
                            print(p_header)
                            print()
                            print(tabulate(selected, headers=p_header, tablefmt=fmt))

                        else:
                            print("\n[!] Error: Invalid Number")
                    except ValueError:
                        print("\n[!] Error: Enter the correct Value\n")
                
                except sq.ProgrammingError:
                    print("\n[!] Error: Enter the correct Value\n")
        
            elif column_count.upper() == "ALL":
                print()
                print(f"SELECT * FROM {table}")
                show_table(table)
                print()

            else:
                print("\n[!] Error: Wrong Command\n")
    else:
        print("\n[!] Error: Wrong Table Name\n")

def insert_values():
    curs = conn.cursor()
    table = input("(HMS: Enter Table Name (patient, doctor)) > ")
    try:
        entries = int(input("(HMS: Enter Number Of Entries) > "))
        try:
            print("\n[&] The Columns Of The Table is as Follows: ")
            curs.execute(f"DESCRIBE {table}")
            table_desc = curs.fetchall()
            columns = {} 
            for i in table_desc:
                if i != table_desc[0]: #Excluding Entry of ID Of Main Tables To Implement AUTO_INCREMENT
                    columns.update({i[0]:i[1].upper()})
            print(f"    {columns}")

            print("\n[&] After every value put a '/' (Example: abcd/efgh/123)")
            print("[&] If you don't have a value, Leave Empty (Example: abc/def//123)")
            print("[&] The format for writing date is (yyyymmdd)")
            for j in range(entries):
                try:
                    entry = tuple(input("\n(HMS: Enter values) > ").split("/"))
                    
                    if not entry:
                        print("[!] Error: No value is entered")
                        break
                    else:
                        if table.upper() == "PATIENT":
                            e=list(entry) #Forms a List Of Entered Values

                            curs.execute("""INSERT INTO patient
                            (First_Name, Last_Name, Age, Date_of_Birth, 
                            Sex, Address, Phone, Insurance_ID, Date_Of_Admission) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", e) #For 9 Columned Row Of Inputs

                            # This is required (Because when we dont have a value it enteres nothing in the db cell, it should enter NULL)
                            curs.execute("""UPDATE patient
                                        SET First_Name=NULL
                                        WHERE First_Name=''""")
                            curs.execute("""UPDATE patient
                                        SET Last_Name=NULL
                                        WHERE Last_Name=''""")
                            curs.execute("""UPDATE patient
                                        SET Age=NULL
                                        WHERE Age=''""")
                            curs.execute("""UPDATE patient
                                        SET Sex=NULL
                                        WHERE Sex=''""")
                            curs.execute("""UPDATE patient
                                        SET Address=NULL
                                        WHERE Address=''""")
                            curs.execute("""UPDATE patient
                                        SET Phone=NULL
                                        WHERE Phone=''""")
                            curs.execute("""UPDATE patient
                                        SET Insurance_ID=NULL
                                        WHERE Insurance_ID=''""")

                            patient_diagnosis = input("(HMS: Patient diagnosed with) > ")
                            print("\n[&] If there is no room number, type 0\n")
                            patient_room = int(input("(HMS: Patient Room (If Any)) > "))
                            treated_by = input("\n(HMS: Treated By) > ")
                                
                            if patient_room != 0:
                                curs.execute(f"INSERT INTO diagnosis(Patient_Diagnosis, Room_Number, Treated_By) VALUES {patient_diagnosis, patient_room, treated_by}")
                                curs.execute("""UPDATE diagnosis
                                        SET Patient_Diagnosis=NULL
                                        WHERE Patient_Diagnosis=''""")
                                curs.execute("""UPDATE diagnosis
                                        SET Treated_By=NULL
                                        WHERE Treated_By=''""")

                            elif patient_room == 0:
                                data_ = (patient_diagnosis, None, treated_by)
                                curs.execute(f"INSERT INTO diagnosis(Patient_Diagnosis, Room_Number, Treated_By) VALUES (%s, %s, %s)", data_)

                        elif table.upper() == "DOCTOR":
                            data=list(entry)
                            curs.execute("""INSERT INTO doctor
                            (First_Name, Last_Name, Specialization,
                            Age, Sex, Address, Phone)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)""",data)
                    
                    commit=input("(Do you want to commit changes?) Y/n > ")
                    if commit.upper() in ["YES", "Y"]:
                        print("\n[+] Database Updated")
                        conn.commit()
                    elif commit.upper() in ["NO", "N"]:
                        print("\n[#] No changes took place")
                    else:
                        print("\n[!] Error: Wrong input")
                        
                except sq.ProgrammingError:
                    print("\n[!] Error: Enter the correct Value")

        except ValueError:
            print("\n[!] Error: Enter the correct Value\n")
    except ValueError:
        print("\n[!] Error: Enter the correct Value")
    
    conn.commit()

def update_data():
    curs=conn.cursor()
    table = input("(HMS: Enter Table Name (patient, doctor, diagnosis)) > ")
    if table.upper() in ["PATIENT", "DOCTOR", "DIAGNOSIS"]:
        curs.execute("SELECT * FROM "+table)
        item=curs.fetchall()
        
        if len(item)==0:
            print("\n[#] No values available (Empty table)\n")

        elif len(item)!=0:
            fmt="double_grid"
            if table.upper()=="PATIENT":
                p_header=["Patient_ID", "First_Name", "Last_Name", "Age", "Date_Of_Birth", "Sex", "Address", "Phone", "Insurance ID", "Date_Of_Admission"]
                print()
                print(tabulate([p_header], tablefmt=fmt))
                print()
            
            elif table.upper()=="DOCTOR":
                doc_header=["Doctor_ID", "First_Name", "Last_Name", "Specialization", "Age", "Sex", "Address", "Phone"]
                print()
                print(tabulate([doc_header], tablefmt=fmt))
                print()
            
            elif table.upper()=="DIAGNOSIS":
                diag_header=["Patient_ID", "Diagnosis", "Room_Number"]
                print()
                print(tabulate([diag_header], tablefmt=fmt))
                print()

            try:
                column_change = input("(HMS: Enter Column Of Record To Update) > ")
                column_value = input("(HMS: Enter Value To Update To) > ")
                change = f"{column_change} = '{column_value}'"
            
                print(f"\n[&] If there are no conditions the whole '{column_change}' column will be changed to '{column_value}'")
                
                try:
                    condition_count = int(input("(HMS: Number Of Conditions) > "))
                    curs.execute(f"UPDATE {table} SET {change}")
                
                    if condition_count == 0:
                        confirm = input(f"\n(HMS: This Will Modify Every Record In '{table}' Table) Commit? Y/n > ")
                        if confirm.upper() in ["YES", "Y"]:
                            conn.commit()
                            print("[+] Database Updated")
                        elif confirm.upper() in ["NO", "N"]:
                            print("[#] Change Reverted")
                        else:
                            print("\n[!] Error: Wrong input")
                    
                    elif condition_count > 0:
                        conditions = ""
                        for i in range(condition_count):
                            condition_column = input(f"(HMS: Enter Column To Use As Condition {i+1}) > ")
                            condition_value = input(f"(HMS: Enter Value To Search With Respect To Column Condition {i+1}) > ")
                            
                            if not condition_value.isdigit():
                                condition_value = f"{condition_value}"
                            conditions += f"{condition_column} = '{condition_value}'"
                            
                            if condition_count == 1:
                                pass
                            elif i == (condition_count - 1):
                                pass
                            else:
                                conditions += " AND "

                        curs.execute(f"UPDATE {table} SET {change} WHERE {conditions}")
                        confirm = input(f"\n(HMS: This Will Modify Every Record In '{table}' Table) Commit? Y/n > ")
                        if confirm.upper() in ["YES", "Y"]:
                            conn.commit()
                            print("\n[+] Database Updated\n")
                        elif confirm.upper() in ["NO", "N"]:
                            print("\n[#] Change Reverted\n")
                        else:
                            print("\n[!] Error: Wrong input")
                    else:
                        print("Something went Wrong")
                    
                except ValueError:
                    print("\n[!] Error: Number of conditions must be interger\n")
                    
            except ValueError:
                print("\n[!] Error: Type the Values correctly\n")
            except sq.ProgrammingError:
                print("\n[!] Error: Enter the values correctly\n")
    else:
        print("\n[!] Error: Wrong Table Name\n")

def remove_value():
    curs=conn.cursor()
    tab=input("(HMS: Enter table name) > ")
    if tab.upper() in ["PATIENT", "DOCTOR", "DIAGNOSIS"]:
        show_table(s_table=tab)

        print("\n•—————————————————————————————•")
        print("   Methods of removing Value")
        print("   1. Specific value")
        print("   2. Complete row")
        print("•—————————————————————————————•\n")

        curs.execute("SELECT * FROM "+tab)
        item=curs.fetchall()
        if len(item)==0:
            print("[#] No values availabe (empty table)\n")
            remove_value()
        elif len(item)!=0:
            # PATIENT
            if tab.upper()=="PATIENT":
                inp_pat=input("(HMS: Choose an Option) > ")
                if inp_pat.upper() in ["1", "SPECIFIC VALUE"]:
                    row_pat=input("(HMS: Enter the Patient ID) > ")
                    column_pat=input("(HMS: Enter the Column Name) > ")

                    curs.execute(f"UPDATE {tab} SET {column_pat}=NULL WHERE Patient_ID={row_pat}")
                    show_table(s_table=tab)

                elif inp_pat.upper() in ["2", "COMPLETE ROW"]:
                    rowp=input("(HMS: Enter the Patient ID you want to remove) > ")
                    curs.execute(f"DELETE FROM {tab} WHERE Patient_ID={rowp}")
                    show_table(s_table=tab)

                else:
                    print("[#] Wrong Option")

            # DOCTOR
            elif tab.upper()=="DOCTOR":
                inp_doc=input("(HMS: Choose an Option) > ")
                if inp_doc.upper() in ["1", "SPECIFIC VALUE"]:
                    row_doc=input("(HMS: Enter the Doctor ID) > ")
                    column_doc=input("(HMS: Enter the Column Name) > ")

                    curs.execute(f"UPDATE {tab} SET {column_doc}=NULL WHERE Doctor_ID={row_doc}")
                    show_table(s_table=tab)

                elif inp_doc in ["2", "COMPLETE ROW"]:
                    _rowD=input("(HMS: Enter the Patient ID you want to remove) > ")
                    curs.execute(f"DELETE FROM {tab} WHERE Doctor_ID={_rowD}")
                    show_table(s_table=tab)
                
                else:
                    print("[#] Wrong Option")
            
            # DIAGNOSIS
            elif tab.upper()=="DIAGNOSIS":
                inp_diag=input("(HMS: Choose an Option) > ")
                if inp_diag.upper() in ["1", "SPECIFIC VALUE"]:
                    row_diag=input("(HMS: Enter the Patient ID) > ")
                    column_diag=input("(HMS: Enter the Column Name) > ")

                    curs.execute(f"UPDATE {tab} SET {column_diag}=NULL WHERE Doctor_ID={row_diag}")
                    show_table(s_table=tab)

                elif inp_diag.upper() in ["2", "COMPLETE ROW"]:
                    rowdi=input("(HMS: Enter the Patient ID you want to remove) > ")
                    curs.execute(f"DELETE FROM {tab} WHERE Patient_ID={rowdi}")
                    show_table(s_table=tab)
                
                else:
                    print("[#] Wrong Option")
            
            else:
                print("[!] Error: No Table Found")

            commit=input("(Do you want to commit changes?) Y/n > ")
            if commit.upper() in ["YES", "Y"]:
                print("\n[+] Database Updated")
                conn.commit()
            elif commit.upper() in ["NO", "N"]:
                print("\n[#] No changes took place")
            else:
                print("\n[!] Error: Wrong input")
    else:
        print("\n[!] Error: Wrong Table Name")

def reset_db():
    curs=conn.cursor()
    curs.execute("DELETE FROM Patient")
    curs.execute("DELETE FROM Doctor")
    curs.execute("DELETE FROM Diagnosis")
    
    print("\n[$] This will result in loss of all data present in the Database Tables\n")
    reset=input("(Do you want to commit changes?) Y/n > ")
    if reset.upper() in ["Y", "YES"]:
        print("\n[+] Database Tables got cleared")
        conn.commit()
    elif reset.upper() in ["N", "NO"]:
        print("\n[#] No changes took place")
    else:
        print("\n[!] Error: Wrong input")

def show_table(s_table):
    if s_table.upper() in ["PATIENT", "DOCTOR", "DIAGNOSIS"]:
        curs=conn.cursor()
        curs.execute("SELECT * FROM "+s_table)
        item=curs.fetchall()
        if len(item)==0:
            print("\n[#] No values availabe (empty table)")
        else:
            fmt="double_grid"
            if s_table.upper()=="PATIENT":
                p_header=["Patient_ID", "First_Name", "Last_Name", "Age", "Date_of_Birth", "Sex", "Address", "Phone", "Insurance_ID", "Date_Of_Admission"]
                print(tabulate(item, headers=p_header, tablefmt=fmt))
            elif s_table.upper()=="DOCTOR":
                doc_header=["Doctor_ID", "First_Name", "Last_Name", "Specialization", "Age", "Sex", "Address", "Phone"]
                print(tabulate(item, headers=doc_header, tablefmt=fmt))
            elif s_table.upper()=="DIAGNOSIS":
                diag_header=["Patient_ID", "Patient_Diagnosis", "Room_Number", "Treated_By"]
                print(tabulate(item, headers=diag_header, tablefmt=fmt))
            else:
                print("[!] Error: Wrong Table Name")
    else:
        print("\n[!] Error: Wrong Table Name\n")

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

    host = input("\n(Login: Hostname) > ")
    user = input("(Login: Username) > ")
    db = input("(Login: Database Name) > ")
    passwd = getpass("(Login: Database Connection Password) > ")
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
            print("""\nDatabase Queries:-
\t1. Describe Table
\t2. Select Data
\t3. Insert Value(s)
\t4. Remove Value(s)
\t5. Update Value(s)
\t6. Show Table
\t7. Reset Database
\t8. Disconnect\n""")

            action = input("(HMS: Enter Command) > ")
            if action.upper() in ("DESCRIBE TABLE", "1"):
                describe_table()
            elif action.upper() in ("SELECT DATA", "SELECT", "2"):
                select_data()
            elif action.upper() in ("INSERT VALUES", "INSERT VALUE", "INSERT", "3"):
                insert_values()
            elif action.upper() in ("REMOVE VALUES", "REMOVE VALUE", "REMOVE", "4"):
                remove_value()
            elif action.upper() in ("UPDATE VALUES", "UPDATE VALUE", "UPDATE", "5"):
                update_data()
            elif action.upper() in ("SHOW TABLE", "6"):
                show_table(s_table = input("(HMS: Enter Table Name (patient, doctor, diagnosis)) > "))
            elif action.upper() in ("RESET DATABASE", "RESET", "7"):
                reset_db()
            elif action.upper() in ("DISCONNECT", "8"):
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
        print("[!] There was an Error", Error)

# this KeyboardInterrupt error happens when u press ctrl+c
except KeyboardInterrupt:
    print("Press any key to exit...")
    # ↓ this line of code takes any keystroke
    msvcrt.getch()
    exit
    print()

# END
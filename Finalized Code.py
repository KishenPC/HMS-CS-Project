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
# [>] - for questions like "do you want to quit" etc.

# Colors
"""
Example:
this changes the color of Abcd and whole terminal
      start
        ↓
print("\033[91mAbcd")

this changes the color of Abcd and ends it there(after Abcd the whole color of terminal becomes default)
      start           End
        ↓              ↓
print("\033[91mAbcd\033[0m")
"""

# Function of HMS
def create_tables():
    curs = conn.cursor()

    curs.execute("""CREATE TABLE Doctor(
        Doctor_ID INT PRIMARY KEY AUTO_INCREMENT,
        First_Name VARCHAR(15),
        Last_Name VARCHAR(15),
        Specialization VARCHAR(30),
        Age INT,
        Gender VARCHAR(6),
        Address VARCHAR(50),
        Phone VARCHAR(11))""")

    curs.execute("""CREATE TABLE Patient(
        Patient_ID INT PRIMARY KEY AUTO_INCREMENT,
        First_Name VARCHAR(15),
        Last_Name VARCHAR(15),
        Age INT,
        Date_of_Birth DATE,
        Gender VARCHAR(6),
        Address VARCHAR(50),
        Phone VARCHAR(11),
        Insurance_ID INT,
        Date_Of_Admission DATE)""")
    
    curs.execute("""CREATE TABLE Diagnosis(
        Patient_ID INT PRIMARY KEY AUTO_INCREMENT,
        Patient_Diagnosis VARCHAR(40),
        Room_Number INT,
        Treated_By VARCHAR(30))""")

# Table Format
fmt="double_grid"

"""
Default: \033[0m
Light Red: \033[91m
Light Green: \033[92m
Light Yellow: \033[93m
Light Blue: \033[94m
Light Magenta: \033[95m
Light Cyan: \033[96m
Light White: \033[97m
Orange: \033[38;5;214m
"""

default="\033[0m"
bold="\033[1m"
underline="\033[4m"

list_heading="\033[38;2;20;0;175m"
login_color="\033[36m"
input_color="\033[38;2;255;0;98m"
table_column_color="\033[94m"
color="\033[38;2;71;165;184m"
added_color="\033[32m"
showing_info_color="\033[38;5;214m"
warning_color="\033[93m"
error_color="\033[91m"
dis="\033[91m"
not_availabe_color="\033[90m"

hms_color=bold+"HMS:"+default
login=bold+"Login:"+default

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
        print(f"\n{error_color}[!] Error: Found Incomplete Database{default}")
        reset = input("(Reset Database?) y/N > ")
        if reset.upper() in ["YES", 'Y']:
            drop_tables()
            create_tables()

        elif reset.upper() in ["NO", 'N']:
            print(f"\n{not_availabe_color}[#] Please Swap to a Different Database{default}")
            conn.close()
        else:
            print(f"{error_color}[!] Wrong Command{default}")

# Functions
# ALL TABLES
def all_tables():
    curs = conn.cursor()
    curs.execute("SHOW TABLES")
    show_tables = curs.fetchall()
    tables = []
    for i in show_tables:
        for z in i: #Due to the fact that returned list of tables in the form [(t1,),(t2,)]
            tables.append(z)
    
    if len(tables) == 0:
        print(f"{not_availabe_color}[#] There Are No Available Tables in Your Database{default}") 
    else:
        print(f"\t{list_heading}•———————————————————•{default}")
        for i in tables:
            print(f"\t{tables.index(i)+1}. {i}")
        print(f"\t{list_heading}•———————————————————•{default}")

# DESCRIBE TABLE
def describe_table():
    curs = conn.cursor()
    table = input(f"({hms_color} {input_color}Enter Table Name To Describe (patient, doctor, diagnosis){default}) > ")
    if table.upper() in ["PATIENT", "DOCTOR", "DIAGNOSIS"]:
        curs.execute(f"DESCRIBE {table}")
        table_desc = curs.fetchall()
        columns = {} 
        print("\n"+ showing_info_color +"[&] The Format Is, {Column Name : Data Type}"+default)
        for i in table_desc:
            columns.update({i[0]:i[1].upper()})
        print(f"    {columns}\n")
    else:
        print(f"\n{error_color}[!] Error: Wrong Table Name{default}")

# SELECT DATA
def select_data():
    # I made the header as an item of the table and remove the header from tabulate so it will look like column names only
    curs=conn.cursor()
    table = input(f"({hms_color} {input_color}Enter Table Name (patient, doctor, diagnosis){default}) > ")
    if table.upper() in ["PATIENT", "DOCTOR", "DIAGNOSIS"]:
        curs.execute("SELECT * FROM "+table)
        item=curs.fetchall()
        
        if table.upper()=="PATIENT":
            p_h=[]
            p_header=["Patient_ID", "First_Name", "Last_Name", "Age", "Date_Of_Birth", "Gender", "Address", "Phone", "Insurance ID", "Date_Of_Admission"]
            for p in p_header:
                p_h.append(f"{table_column_color}{p}{default}")
            print()
            print(tabulate([p_h], tablefmt=fmt))
            print()
        
        elif table.upper()=="DOCTOR":
            doc_h=[]
            doc_header=["Doctor_ID", "First_Name", "Last_Name", "Specialization", "Age", "Gender", "Address", "Phone"]
            for doc in doc_header:
                doc_h.append(f"{table_column_color}{doc}{default}")
            print()
            print(tabulate([doc_h], tablefmt=fmt))
            print()
        
        elif table.upper()=="DIAGNOSIS":
            diag_h=[]
            diag_header=["Patient_ID", "Diagnosis", "Room_Number"]
            for diag in diag_header:
                diag_h.append(f"{table_column_color}{diag}{default}")
            print()
            print(tabulate([diag_h], tablefmt=fmt))
            print()
        
        if len(item)==0:
            print(f"{not_availabe_color}[#] No values availabe (Empty table){default}")
        
        elif len(item) != 0:
            column_count = input(f"({hms_color} {input_color}Columns to Display (Selective/All){default}) > ")
            if column_count.upper() == "SELECTIVE":
                try:
                    columns = input(f"({hms_color} {input_color}Enter The Name Of The Columns Seperated By Comma{default}) > ")
                    try:
                        condition_count = int(input(f"({hms_color} {input_color}Number Of Conditions{default}) > "))
                        
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
                                condition_column = input(f"({hms_color} {input_color}Enter Column To Use As Condition {i+1}{default}) > ")
                                condition_value = input(f"({hms_color} {input_color}Enter Value To Search With Respect To Column Condition {i+1}{default}) > ")
                                
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
                            print(f"\n{error_color}[!] Error: Invalid Number{default}")
                    except ValueError:
                        print(f"\n{error_color}[!] Error: Enter the correct Value{default}\n")
                
                except sq.ProgrammingError:
                    print(f"\n{error_color}[!] Error: Enter the correct Value{default}\n")
        
            elif column_count.upper() == "ALL":
                print()
                print(f"SELECT * FROM {table}")
                show_table(table)
                print()

            else:
                print(f"\n{error_color}[!] Error: Wrong Command{default}\n")
    else:
        print(f"\n{error_color}[!] Error: Wrong Table Name{default}\n")

# INSERT VALUES
def insert_values():
    curs = conn.cursor()
    table = input(f"({hms_color} {input_color}Enter Table Name (patient, doctor){default}) > ")
    try:
        entries = int(input(f"({hms_color} {input_color}Enter Number Of Entries{default}) > "))
        try:
            print(f"\n{showing_info_color}[&] The Columns Of The Table is as Follows: {default}")
            curs.execute(f"DESCRIBE {table}")
            table_desc = curs.fetchall()
            columns = {} 
            for i in table_desc:
                if i != table_desc[0]: #Excluding Entry of ID Of Main Tables To Implement AUTO_INCREMENT
                    columns.update({i[0]:i[1].upper()})
            print(f"    {columns}")

            print(f"\n{showing_info_color}[&] After every value put a '/' (Example: abcd/efgh/123){default}")
            print(f"{showing_info_color}[&] There is no need of typing the Patient_ID{default}")
            print(f"{showing_info_color}[&] If you don't have a value, Leave Empty (Example: abc/def//123){default}")
            print(f"{showing_info_color}[&] The format for writing date is (yyyymmdd){default}\n")
            for j in range(entries):
                try:
                    show_table(table)
                    entry = tuple(input(f"\n({hms_color} {input_color}Enter values{default}) > ").split("/"))
                    
                    if not entry:
                        print(f"{error_color}[!] Error: No value is entered{default}")
                        break
                    else:
                        if table.upper() == "PATIENT":
                            e=list(entry) #Forms a List Of Entered Values

                            curs.execute("""INSERT INTO patient
                            (First_Name, Last_Name, Age, Date_of_Birth, 
                            Gender, Address, Phone, Insurance_ID, Date_Of_Admission) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", e) #For 9 Columned Row Of Inputs

                            # This is required (Because when we dont have a value it enteres nothing in the db cell, it should enter NULL)
                            col=["Patinet_ID", "First_Name", "Last_Name", "Age", "Gender", "Insrance_ID", "Date_Of_Birth", "Address", "Phone", "Date_Of_Admission"]
                            for it in col:
                                query=f"""UPDATE patient
                                            SET {it}=NULL
                                            WHERE {it}=''"""
                                try:
                                    curs.execute(query)
                                except:
                                    pass
                            
                            patient_diagnosis = input(f"({hms_color} {input_color}Patient diagnosed with{default}) > ")
                            print(f"\n{showing_info_color}[&] If there is no room number, type 0{default}")
                            patient_room = int(input(f"({hms_color} {input_color}Patient Room (If Any){default}) > "))
                            treated_by = input(f"({hms_color} {input_color}Treated By{default}) > ")
                                
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
                            Age, Gender, Address, Phone)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)""", data)
                    
                    commit=input("(Do you want to commit changes?) Y/n > ")
                    if commit.upper() in ["YES", "Y"]:
                        print(f"\n{added_color}[+] Database Updated{default}")
                        conn.commit()
                    elif commit.upper() in ["NO", "N"]:
                        print(f"\n{not_availabe_color}[#] No changes took place{default}")
                    else:
                        print(f"\n{error_color}[!] Error: Wrong input{default}")
                        
                except sq.ProgrammingError:
                    print(f"\n{error_color}[!] Error: Enter the correct Value{default}")

        except ValueError:
            print(f"\n{error_color}[!] Error: Enter the correct Value{default}\n")
    except ValueError:
        print(f"\n{error_color}[!] Error: Enter the correct Value{default}")

# UPDATE DATA
def update_data():
    curs=conn.cursor()
    table = input(f"({hms_color} {input_color}Enter Table Name (patient, doctor, diagnosis){default}) > ")
    if table.upper() in ["PATIENT", "DOCTOR", "DIAGNOSIS"]:
        curs.execute("SELECT * FROM "+table)
        item=curs.fetchall()
        
        if len(item)==0:
            print(f"\n{not_availabe_color}[#] No values available (Empty table){default}\n")

        elif len(item)!=0:
            if table.upper()=="PATIENT":
                p_header=["Patient_ID", "First_Name", "Last_Name", "Age", "Date_Of_Birth", "Gender", "Address", "Phone", "Insurance ID", "Date_Of_Admission"]
                print()
                print(tabulate([p_header], tablefmt=fmt))
                print()
            
            elif table.upper()=="DOCTOR":
                doc_header=["Doctor_ID", "First_Name", "Last_Name", "Specialization", "Age", "Gender", "Address", "Phone"]
                print()
                print(tabulate([doc_header], tablefmt=fmt))
                print()
            
            elif table.upper()=="DIAGNOSIS":
                diag_header=["Patient_ID", "Diagnosis", "Room_Number"]
                print()
                print(tabulate([diag_header], tablefmt=fmt))
                print()

            try:
                column_change = input(f"({hms_color} {input_color}Enter Column Of Record To Update{default}) > ")
                column_value = input(f"({hms_color} {input_color}Enter Value To Update To{default}) > ")
                change = f"{column_change} = '{column_value}'"
            
                print(f"\n{showing_info_color}[&] If there are no conditions the whole '{column_change}' column will be changed to '{column_value}'{default}")
                
                try:
                    condition_count = int(input(f"({hms_color} {input_color}Number Of Conditions{default}) > "))
                    curs.execute(f"UPDATE {table} SET {change}")
                
                    if condition_count == 0:
                        confirm = input(f"\n({hms_color} {input_color}This Will Modify Every Record In '{table}' Table{default}) Commit? Y/n > ")
                        if confirm.upper() in ["YES", "Y"]:
                            conn.commit()
                            print(f"{added_color}[+] Database Updated{default}")
                        elif confirm.upper() in ["NO", "N"]:
                            print(f"{not_availabe_color}[#] Change Reverted{default}\n")
                        else:
                            print(f"\n{error_color}[!] Error: Wrong input{default}")
                    
                    elif condition_count > 0:
                        conditions = ""
                        for i in range(condition_count):
                            condition_column = input(f"({hms_color} {input_color}Enter Column To Use As Condition {i+1}{default}) > ")
                            condition_value = input(f"({hms_color} {input_color}Enter Value To Search With Respect To Column Condition {i+1}{default}) > ")
                            
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
                        confirm = input(f"\n({hms_color} {input_color}This Will Modify Every Record In '{table}' Table{default}) Commit? Y/n > ")
                        if confirm.upper() in ["YES", "Y"]:
                            conn.commit()
                            print(f"\n{added_color}[+] Database Updated{default}\n")
                        elif confirm.upper() in ["NO", "N"]:
                            print(f"\n{not_availabe_color}[#] Change Reverted{default}\n")
                        else:
                            print(f"\n{error_color}[!] Error: Wrong input{default}")
                    else:
                        print("Something went Wrong")
                    
                except ValueError:
                    print(f"\n{error_color}[!] Error: Number of conditions must be interger{default}\n")
                    
            except ValueError:
                print(f"\n{error_color}[!] Error: Type the Values correctly{default}\n")
            except sq.ProgrammingError:
                print(f"\n{error_color}[!] Error: Enter the values correctly{default}\n")
    else:
        print(f"\n{error_color}[!] Error: Wrong Table Name{default}\n")

# REMOVE VALUE
def remove_value():
    curs=conn.cursor()
    tab=input(f"({hms_color} {input_color}Enter table name{default}) > ")
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
            print(f"{not_availabe_color}[#] No values availabe (Empty table){default}\n")
            remove_value()
        elif len(item)!=0:
            # PATIENT
            if tab.upper()=="PATIENT":
                inp_pat=input(f"({hms_color} {input_color}Choose an Option{default}) > ")
                if inp_pat.upper() in ["1", "SPECIFIC VALUE"]:
                    row_pat=input(f"({hms_color} {input_color}Enter the Patient ID{default}) > ")
                    column_pat=input(f"({hms_color} {input_color}Enter the Column Name{default}) > ")

                    curs.execute(f"UPDATE {tab} SET {column_pat}=NULL WHERE Patient_ID={row_pat}")
                    show_table(s_table=tab)

                elif inp_pat=="2" or inp_pat.upper()=="COMPLETE ROW":
                    rowp=input(f"({hms_color} {input_color}Enter the Patient ID you want to remove{default}) > ")
                    curs.execute(f"DELETE FROM {tab} WHERE Patient_ID={rowp}")
                    show_table(s_table=tab)

                else:
                    print(f"{error_color}[!] Error: Wrong Option{default}")
            
            # DOCTOR
            elif tab.upper()=="DOCTOR":
                inp_doc=input(f"({hms_color} {input_color}Choose an Option{default}) > ")
                if inp_doc.upper() in ["1", "SPECIFIC VALUE"]:
                    row_doc=input(f"({hms_color} {input_color}Enter the Doctor ID{default}) > ")
                    column_doc=input(f"({hms_color} {input_color}Enter the Column Name{default}) > ")

                    curs.execute(f"UPDATE {tab} SET {column_doc}=NULL WHERE Doctor_ID={row_doc}")
                    show_table(s_table=tab)

                elif inp_doc=="2" or inp_doc.upper()=="COMPLETE ROW":
                    _rowD=input(f"({hms_color} {input_color}Enter the Patient ID you want to remove{default}) > ")
                    curs.execute(f"DELETE FROM {tab} WHERE Doctor_ID={_rowD}")
                    show_table(s_table=tab)
                
                else:
                    print(f"{error_color}[!] Error: Wrong Option{default}")
            
            # DIAGNOSIS
            elif tab.upper()=="DIAGNOSIS":
                inp_diag=input(f"({hms_color} {input_color}Choose an Option{default}) > ")
                if inp_diag.upper() in ["1", "SPECIFIC VALUE"]:
                    row_diag=input(f"({hms_color} {input_color}Enter the Patient ID{default}) > ")
                    column_diag=input(f"({hms_color} {input_color}Enter the Column Name{default}) > ")

                    curs.execute(f"UPDATE {tab} SET {column_diag}=NULL WHERE Doctor_ID={row_diag}")
                    show_table(s_table=tab)

                elif inp_diag=="2" or inp_diag.upper()=="COMPLETE ROW":
                    rowdi=input(f"({hms_color} {input_color}Enter the Patient ID you want to remove{default}) > ")
                    curs.execute(f"DELETE FROM {tab} WHERE Patient_ID={rowdi}")
                    show_table(s_table=tab)
                
                else:
                    print(f"{error_color}[#] Wrong Option{default}")
            
            else:
                print(f"{error_color}[!] Error: No Table Found{default}")

            commit=input("(Do you want to commit changes?) Y/n > ")
            if commit.upper() in ["YES", "Y"]:
                print(f"\n{added_color}[+] Database Updated{default}")
                conn.commit()
            elif commit.upper() in ["NO", "N"]:
                print(f"\n{not_availabe_color}[#] No changes took place{default}")
            else:
                print(f"\n{error_color}[!] Error: Wrong input{default}")
    else:
        print(f"\n{error_color}[!] Error: Wrong Table Name{default}")

# RESET DB
def reset_db():
    curs=conn.cursor()
    curs.execute("DELETE FROM Patient")
    curs.execute("DELETE FROM Doctor")
    curs.execute("DELETE FROM Diagnosis")
    
    print(f"\n{warning_color}[$] This will result in loss of all data present in the Database Tables{default}\n")
    reset=input("(Do you want to commit changes?) Y/n > ")
    if reset.upper() in ["Y", "YES"]:
        print(f"\n{added_color}[+] Database Tables got cleared{default}")
        conn.commit()
    elif reset.upper() in ["N", "NO"]:
        print(f"\n{not_availabe_color}[#] No changes took place{default}")
    else:
        print(f"\n{error_color}[!] Error: Wrong input{default}")

# SHOW TABLE
def show_table(s_table):
    if s_table.upper() in ["PATIENT", "DOCTOR", "DIAGNOSIS"]:
        curs=conn.cursor()
        curs.execute("SELECT * FROM "+s_table)
        item=curs.fetchall()
        if len(item)==0:
            print(f"\n{not_availabe_color}[#] No values availabe (Empty table){default}")
        else:
            if s_table.upper()=="PATIENT":
                p_h=[]
                p_header=["Patient_ID", "First_Name", "Last_Name", "Age", "Date_of_Birth", "Gender", "Address", "Phone", "Insurance_ID", "Date_Of_Admission"]
                for p in p_header:
                    p_h.append(f"{table_column_color}{p}{default}")
                print(tabulate(item, headers=p_h, tablefmt=fmt))

            elif s_table.upper()=="DOCTOR":
                doc_h=[]
                doc_header=["Doctor_ID", "First_Name", "Last_Name", "Specialization", "Age", "Gender", "Address", "Phone"]
                for doc in doc_header:
                    doc_h.append(f"{table_column_color}{doc}{default}")
                print(tabulate(item, headers=doc_h, tablefmt=fmt))

            elif s_table.upper()=="DIAGNOSIS":
                diag_h=[]
                diag_header=["Patient_ID", "Patient_Diagnosis", "Room_Number", "Treated_By"]
                for diag in diag_header:
                    diag_h.append(f"{table_column_color}{diag}{default}")
                print(tabulate(item, headers=diag_h, tablefmt=fmt))
            else:
                print(f"{error_color}[!] Error: Wrong Table Name{default}")
    else:
        print(f"\n{error_color}[!] Error: Wrong Table Name{default}\n")

# Code
welcome_text_color="\033[95m"
start_color="\033[92m"

col="\033[32m"
print(f"\n{bold}{col}[@] Starting the Hospital Management System Console.../{default}")
time.sleep(0.5)

print("\n"+"="*81)
print(f"  [{start_color}Project{default}] Hospital Management System")
print("="*81)

print(f"  [{start_color}Credits{default}] Abin Krishna, Kishen PC, MP Vaishak Anoop Nambiar")
print("="*81+"""\033[37m
            
                       ██╗  ██╗    ███╗   ███╗    ███████╗
                       ██║  ██║    ████╗ ████║    ██╔════╝
                       ███████║    ██╔████╔██║    ███████╗
                       ██╔══██║    ██║╚██╔╝██║    ╚════██║
                       ██║  ██║    ██║ ╚═╝ ██║    ███████║
                       ╚═╝  ╚═╝    ╚═╝     ╚═╝    ╚══════╝
""")

try:
    print(f"\t\t{bold}       {underline}Enter SQL Server Connection Details{default}\n")
    print("—"*81)

    host = input(f"\n({login} {login_color}Hostname{default}) > ")
    user = input(f"({login} {login_color}Username{default}) > ")
    db = input(f"({login} {login_color}Database Name{default}) > ")
    passwd = getpass(f"({login} {login_color}Database Connection Password{default}) > ")
    # By using "getpass" whenever u type the password it will be hidden in the terminal
    
    conn = sq.connect(host=host, username=user , database=db, passwd=passwd)
    
    if conn.is_connected():
        time.sleep(1)
        print(f"\n{bold}{welcome_text_color}[⁎] Connected to {host}{default}")
        print(f"{bold}{welcome_text_color}[⁎] Welcome To The {db} Databse Interface{default}\n")
        print(f"{list_heading}List of Tables:-{default}")
        hosptial_db_setup()
        all_tables()

        while conn.is_connected():
            print(f"""\n{list_heading}Database Queries:-{default}

\t{list_heading}•———————————————————•{default}
 \t1. Describe Table
 \t2. Select Data
 \t3. Insert Value(s)
 \t4. Update Value(s)
 \t5. Remove Value(s)
 \t6. Show table
 \t7. Reset Database
 \t8. Disconnect
\t{list_heading}•———————————————————•{default}\n""")

            action = input(f"({hms_color} {input_color}Enter Command{default}) > ")
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
                show_table(s_table = input(f"({hms_color} {input_color}Enter Table Name (patient, doctor, diagnosis){default}) > "))
            elif action.upper() in ("RESET DATABASE", "RESET", "7"):
                reset_db()
            
            elif action.upper() in ("DISCONNECT", "8"):
                con_quit=input(f"{dis}[>] Do you wish to Disconnect? Enter 'q' to exit: {default}")
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
                print("\t?\t\talias for help")
                print("\tclear\t\tClears the screen")
                print("\n\texit\t\tExit the console")
            elif action.upper()=="CLEAR":
                os.system("cls")
            elif action.upper()=="EXIT":
                conn.close()
                print()
            
            else:
                print(f"{error_color}[—] Unknown command{default}")

# Interface error(is the server is not running)
except sq.InterfaceError:
    print(f"\n{error_color}[!] Error: Check if the Server is running or not{default}")
    print(f"{error_color}Or make sure you have entered the correct Hostname{default}\n")
# This works only if the credentials are wrong
except sq.Error as err:
    if err.errno==sq.errorcode.ER_ACCESS_DENIED_ERROR:
        print(f"\n{error_color}[!] Access Denied{default}")
        print(f"{error_color}[!] Make sure you have entered the right credentials for the database connection{default}\n")
    else:
        print(f"{error_color}[!] Something Went Wrong{default}\n")

# this KeyboardInterrupt error happens when u press ctrl+c
except KeyboardInterrupt:
    print(f"{error_color}[>] Press any key to exit...{default}")
    # ↓ this line of code takes any keystroke
    msvcrt.getch()
    exit
    print()

# END

import mysql.connector as sq

def create_tables():
    conn_cursor = conn.cursor()
    conn_cursor.execute("""CREATE TABLE patient(
        Patient_ID INT PRIMARY KEY AUTO_INCREMENT,
        Patient_Name VARCHAR(30),
        Patient_Age INT,
        Patient_Gender VARCHAR(7),
        Address VARCHAR(50),
        Phone INT,
        Insurance_ID INT)""")
    conn_cursor.execute("""CREATE TABLE Doctor(
        Doctor_ID INT PRIMARY KEY AUTO_INCREMENT,
        Doctor_Name VARCHAR(30),
        Specialization VARCHAR(30),
        Doctor_Age INT,
        Doctor_Gender VARCHAR(20),
        Address VARCHAR(50),
        Phone INT)""") 
    conn_cursor.execute("""CREATE TABLE Diagnosis(
         Patient_ID INT PRIMARY KEY AUTO_INCREMENT,
        Patient_Diagnosis VARCHAR(100),
        Room_Number INT)""")
#&
#-------------------
#&
def drop_tables():
    conn_cursor = conn.cursor()
    conn_cursor.execute("SHOW TABLES")
    listed_tables = conn_cursor.fetchall()
    tables = []
    for i in listed_tables: #Due to the fact that returned list of tables in the form [(t1,),(t2,)]
        for z in i:
            tables.append(z)
    drop_tables = f"DROP TABLE {tables[0]}"

    if len(tables) == 1:
        conn_cursor.execute(drop_tables)
    else:
        for i in tables[1:]:
            drop_tables += f", {i}"
        conn_cursor.execute(drop_tables)
    conn.commit()
#&
#-------------------
#&

def describe_table():
    conn_cursor = conn.cursor()
    table = input("Enter Name Of Table To Describe > ").lower()
    conn_cursor.execute(f"DESCRIBE {table}")
    table_desc = conn_cursor.fetchall()
    columns = {} 
    #
    print("\nThe Format Is, {Column Name : Data Type}")
    for i in table_desc:
        columns.update({i[0]:i[1].upper()})
    print(f"{columns}\n")
    #
    conn.commit()
#&
#-------------------
#&
def show_tables():
    conn_cursor = conn.cursor()
    conn_cursor.execute("SHOW TABLES")
    show_tables = conn_cursor.fetchall()
    tables = []
    for i in show_tables:
        for z in i: #Due to the fact that returned list of tables in the form [(t1,),(t2,)]
            tables.append(z)
    #
    if len(tables) == 0:
        print("""\nThere Are No Available Tables in Your Database
        Attempting Repair ...""") 
        create_tables()
    #
    else:
        print("\n\t\t___________________")
        print("\t\tList of Tables\n")
        for i in tables:
            print(f"\t\t{tables.index(i)+1}| {i}")
        print("\t\t___________________")
    #
    conn.commit()
#&
#-------------------
#&
def insert_values():
    conn_cursor = conn.cursor()
    table = input("Table Name >")
    entries = int(input("Number Of Entries > "))
    #
    print(f"The Columns Of The Table {table} is as Follows: ")
    conn_cursor.execute(f"DESCRIBE {table}")
    table_desc = conn_cursor.fetchall()
    columns_datatype = {}
    for i in table_desc:
        if i[0].upper() in ("PATIENT ID","DOCTOR_ID","PATIENT_ID"):
            pass
        else:
            columns_datatype.update({i[0]:i[1].upper()})
    columns = [i for i in columns_datatype]
    print(f"{columns}\n")
    #
    print("Enter The Values In Order Seperated By </> ~ A/B/C/1/2 >")
    for i in range(entries):
        entry = list(input().split("/"))
        if table.upper() == "PATIENT":        
            entry[1] = int(entry[1]); entry[4] = int(entry[4]); entry[5] = int(entry[5])
            patient_diagnosis = input("Enter Patient Diagnosis >")
            patient_room = int(input("Enter Patient Room (If Any) >"))
            conn_cursor.execute(f"INSERT INTO patient(Patient_Name, Patient_Age, Patient_Gender, Address, Phone, Insurance_ID) VALUES {tuple(entry)}")
            conn_cursor.execute(f"INSERT INTO diagnosis(Patient_Diagnosis,Room_Number) VALUES {(patient_diagnosis,patient_room)}") #Under Maintenance
        elif table.upper() == "DOCTOR":
            entry[2]=int(entry[2]); entry[5]=int(entry[5])
            conn_cursor.execute(f"INSERT INTO {table}(Doctor_Name, Specialization, Doctor_Age, Doctor_Gender, Address, Phone) VALUES {tuple(entry)}") #Under Maintenance
    #
    conn.commit()
#&
#-------------------
#&
def hosptial_db_setup():
    conn_cursor = conn.cursor()
    conn_cursor.execute("SHOW TABLES")
    show_tables = conn_cursor.fetchall()
    conn.commit()
    tables = []

    for i in show_tables:
        for z in i: #Due to the fact that returned list of tables in the form [(t1,),(t2,)]
            tables.append(z)

    if 'patient' in tables and 'doctor' in tables and  "diagnosis" in tables:
        print("\n")

    elif 'patient' not in tables and 'doctor' not in tables and  "diagnosis" not in tables:
        create_tables()
        #
        conn.commit()  # Complete

    else:
        print("\n⚠ Found Incomplete Database ⚠")
        reset = input("Reset Database? (Yes/No) > ")
        if reset.upper() == "YES":
            drop_tables()
            #
            create_tables()

        elif reset.upper() == "NO":
            print("\n!Please Swap to a Different Database!")
            conn.close()
#&
#-------------------
#&
def reset_db():
    conn_cursor = conn.cursor()
    print("\nThis will result in loss of all data present in the Database Tables")
    reset = input("Proceed With Reset? (Yes/No) > ")
    if reset.upper() == "YES":
        #
        drop_tables()
        create_tables()
        #
        print("\n✓ Successful Database Reset ✓")
        show_tables()
        
    elif reset.upper() == "NO":
        print("\nDatabase Reset Cancelled")

    else:
        print("\nInvalid Input")
#&
"""-----------------------------------------------   Main  -----------------------------------------------"""
#&
try:
    print("\n\t\t\tEnter SQL Server Connection Details")
    print("_"*91)
    host = input("Host Name > ")
    user = input("User Name > ")
    db = input("Database Name > ")
    passwd = input("Database Password > ")
    conn = sq.connect(host=host, user=user , database=db, passwd=passwd)

    if conn.is_connected():
        print("\n✓ HMS Connection Established! ✓")
        print("_"*91)

        print(f"\n-✧˖° Welcome To The HMS Databse Interface ˖°.✧-")
        hosptial_db_setup()
        show_tables()
        
        while conn.is_connected():
            print("""\nHMS Commands:-
            1| Table Details
            2| Record Data
            3| Disconnect
            4| Reset""")

            action = input("\nEnter Command > ")
            if action.upper() == "DISCONNECT":
                conn.close()
            if action.upper() == "TABLE DETAILS":
                describe_table()
            if action.upper() == "RECORD DATA":
                insert_values()
                print("\nValues Recorded!")
            if action.upper() == "RESET":
                reset_db()
                pass #Continue Here

except sq.Error:
    print("\n✘ Connection Failed! ✘")
    print(sq.Error)
    print("Make sure you have entered the right credentials for the database connection")

def describe_table():
    conn_cursor = conn.cursor()
    table = input("Enter Name Of Table To Describe: ").lower()
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
    table = input("Table Name: ")
    entries = int(input("Number Of Entries: "))
    print(f"The Columns Of The Table {table} is as Follows: ")
    conn_cursor.execute(f"DESCRIBE {table}")
    table_desc = conn_cursor.fetchall()
    columns_datatype = {}
    columns = [i for i in columns_datatype]
    print(columns_datatype)
    for i in table_desc:
        columns.update({i[0]:i[1].upper()})
    print(f"{columns_datatype}\n")
    print("Enter The Values In Order Seperated By / ~ [A,B,C,1,2]")
    for i in range(entries):
        entry = list(input().split("/"))
        if table.upper() == "PATIENT":
            entry[0]=int(entry[0]) ; entry[2]=int(entry[2]) ; entry[5]=int(entry[5]) ; entry[6]=int(entry[6])
        elif table.upper() == "DOCTOR":
            entry[0]=int(entry[0]) ; entry[3]=int(entry[3]); entry[5]=int(entry[6])
        elif table.upper() == "PATIENT_CONDITION":
            entry[0]=int(entry[0]) ; entry[2]=int(entry[2])
        conn_cursor.execute(f"INSERT INTO {table} VALUES {tuple(entry)}") #Under Maintenance
    conn.commit()
    

        
def create_hosptial_db():
    conn_cursor = conn.cursor()
    conn_cursor.execute("SHOW TABLES")
    show_tables = conn_cursor.fetchall()
    conn.commit()
    tables = []
    print("TESTING")
    for i in show_tables:
        for z in i: #Due to the fact that returned list of tables in the form [(t1,),(t2,)]
            tables.append(z)
    if 'patient' in tables and 'doctor' in tables and  "patient_condition" in tables:
        print("")
    elif 'patient' not in tables and 'doctor' not in tables and  "patient_condition" not in tables:
        conn_cursor.execute("CREATE TABLE patient(Patient_ID INT PRIMARY KEY AUTO_INCREMENT, Patient_Name VARCHAR(30), Patient_Age INT, Patient_Gender VARCHAR(7), Address VARCHAR(50), Phone INT, Insurance_ID INT)")
        conn_cursor.execute("CREATE TABLE doctor(Doctor_ID INT PRIMARY KEY AUTO_INCREMENT, Doctor_Name VARCHAR(30), Specialization VARCHAR(30), Patient_Age INT, Doctor_Gender VARCHAR(7), Address VARCHAR(50), Phone INT)") 
        conn_cursor.execute("CREATE TABLE patient_condition(Patient_ID INT PRIMARY KEY AUTO_INCREMENT, Diagnosis VARCHAR(100), Room_Number INT)")
        conn.commit()  # COMPLETE DO NOT TOUCH, ALSO CHANGE INPUTTING VALUE CODE ACCORDINGLY
        

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
        print("\n✓ HMS Connection Established! ✓")
        print("_"*91)

        print(f"\n-✧˖° Welcome To The HMS Databse Interface ˖°.✧-")
        create_hosptial_db()
        show_tables()
        
        while conn.is_connected():
            print("""\n_________________\nDatabase Queries:-
            1| Table Details
            2| Record Data
            3| Disconnect""")

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

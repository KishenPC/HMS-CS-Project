######################Abin Krishna###########################

# Function of HMS
def create_tables():
    curs = conn.cursor()

    curs.execute("""CREATE TABLE Doctor(
        Doctor_ID INT PRIMARY KEY AUTO_INCREMENT,
        First_Name VARCHAR(15),
        Last_Name VARCHAR(15),
        Specialization VARCHAR(30),
        Doctor_Age INT,
        Sex VARCHAR(6),
        Address VARCHAR(50),
        Phone VARCHAR(11))""")

    curs.execute("""CREATE TABLE Patient(
        Patient_ID INT PRIMARY KEY AUTO_INCREMENT,
        First_Name VARCHAR(15),
        Last_Name VARCHAR(15),
        Patient_Age INT,
        Date_of_Birth DATE,
        Sex VARCHAR(6),
        Address VARCHAR(50),
        Phone VARCHAR(11),
        Insurance_ID INT,
        Admission_Date DATE)""")
    
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
        if reset.upper() == "YES" or reset==['y', 'Y']:
            drop_tables()
            create_tables()

        elif reset.upper() == "NO" or reset==['n', 'N']:
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
    curs.execute(f"DESCRIBE {table}")
    table_desc = curs.fetchall()
    columns = {} 
    print("\n[&] The Format Is, {Column Name : Data Type}")
    for i in table_desc:
        columns.update({i[0]:i[1].upper()})
    print(f"    {columns}\n")

def select_data():
    pass

def insert_values():
    curs = conn.cursor()
    table = input("(HMS: Enter Table Name (patient, doctor)) > ")
    entries = int(input("(HMS: Enter Number Of Entries) > "))

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
    print("[&] The format for writing date is (yyyymmdd)\n")
    for j in range(entries):
        entry = tuple(input("(HMS: Enter values) > ").split("/"))
        
        if not entry:
            print("[!] Error: No value is entered")
            break
        else:
            if table.upper() == "PATIENT":
                e=list(entry) #Forms a List Of Entered Values

                curs.execute("""INSERT INTO patient
                (First_Name, Last_Name, Patient_Age, Date_of_Birth, 
                Sex, Address, Phone, Insurance_ID, Admission_Date) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", e) #For 9 Columned Row Of Inputs

                # This is required (Because when we dont have a value it enteres nothing in the db cell, it should enter NULL)
                curs.execute("""UPDATE patient
                            SET First_Name=NULL
                            WHERE First_Name=''""")
                curs.execute("""UPDATE patient
                            SET Last_Name=NULL
                            WHERE Last_Name=''""")
                curs.execute("""UPDATE patient
                            SET Patient_Age=NULL
                            WHERE Patient_Age=''""")
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
                Doctor_Age, Sex, Address, Phone)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",data)

    commit=input("(Do you want to commit changes?) Y/n > ")
    if commit.upper() in ["YES", "Y"]:
        print("\n[+] New values got added into the database")
        conn.commit()
    elif commit.upper() in ["NO", "N"]:
        print("\n[#] No changes took place")
    else:
        print("\n[!] Error: Wrong input")

def remove_value():
    curs=conn.cursor()
    tab=input("(HMS: Enter table name) > ")
    show_table(s_table=tab)

    print("\n•—————————————————————————————•")
    print("   Methods of removing Value")
    print("   1. A specific value")
    print("   2. Complete row")
    print("•—————————————————————————————•\n")

    # PATIENT
    curs.execute("SELECT * FROM "+tab)
    item=curs.fetchall()
    if len(item)==0:
        print("[#] No values availabe (empty table)\n")
        remove_value()

    elif tab.upper()=="PATIENT":
        inp_pat=input("(HMS: Choose an Option) > ")
        if inp_pat=="1" or inp_pat.upper()=="A SPECIFIC VALUE":
            row_pat=input("(HMS: Enter the Patient ID) > ")
            column_pat=input("(HMS: Enter the Column Name) > ")

            curs.execute(f"UPDATE {tab} SET {column_pat}=NULL WHERE Patient_ID={row_pat}")
            show_table(s_table=tab)

        elif inp_pat=="2" or inp_pat.upper()=="COMPLETE ROW":
            rowp=input("(HMS: Enter the Patient ID you want to remove) > ")
            curs.execute(f"DELETE FROM pat WHERE Patient_ID={rowp}")
            show_table(s_table=tab)

        else:
            print("[#] Wrong Option")
    
    # DOCTOR
    elif tab.upper()=="DOCTOR":
        inp_doc=input("(HMS: Choose an Option) > ")
        if inp_doc=="1" or inp_doc.upper()=="A SPECIFIC VALUE":
            row_doc=input("(HMS: Enter the Doctor ID) > ")
            column_doc=input("(HMS: Enter the Column Name) > ")

            curs.execute(f"UPDATE {tab} SET {column_doc}=NULL WHERE Doctor_ID={row_doc}")
            show_table(s_table=tab)

        elif inp_doc=="2" or inp_doc.upper()=="COMPLETE ROW":
            _rowD=input("(HMS: Enter the Patient ID you want to remove) > ")
            curs.execute(f"DELETE FROM {tab} WHERE Doctor_ID={_rowD}")
            show_table(s_table=tab)
        
        else:
            print("[#] Wrong Option")
    
    # DIAGNOSIS
    elif tab.upper()=="DIAGNOSIS":
        inp_diag=input("(HMS: Choose an Option) > ")
        if inp_diag=="1" or inp_diag.upper()=="A SPECIFIC VALUE":
            row_diag=input("(HMS: Enter the Patient ID) > ")
            column_diag=input("(HMS: Enter the Column Name) > ")

            curs.execute(f"UPDATE {tab} SET {column_diag}=NULL WHERE Doctor_ID={row_diag}")
            show_table(s_table=tab)

        elif inp_diag=="2" or inp_diag.upper()=="COMPLETE ROW":
            rowdi=input("(HMS: Enter the Patient ID you want to remove) > ")
            curs.execute(f"DELETE FROM {tab} WHERE Patient_ID={rowdi}")
            show_table(s_table=tab)
        
        else:
            print("[#] Wrong Option")
    
    else:
        print("[!] No Table Found")

    commit=input("(Do you want to commit changes?) Y/n > ")
    if commit.upper() in ["YES", "Y"]:
        print("\n[+] New values got added into the database")
        conn.commit()
    elif commit.upper() in ["NO", "N"]:
        print("\n[#] No changes took place")
    else:
        print("\n[!] Error: Wrong input")

def reset_db():
    curs=conn.cursor()
    curs.execute("DELETE FROM Patient")
    curs.execute("DELETE FROM Doctor")
    curs.execute("DELETE FROM Diagnosis")
    
    print("\n[$] This will result in loss of all data present in the Database Tables\n")
    reset=input("(Do you want to commit changes?) Y/n > ")
    if reset in ["y", "Y"] or reset.upper()=="YES":
        print("\n[+] Database Tables got cleared")
        conn.commit()
    elif reset in ["n", "N"] or reset.upper()=="NO":
        print("\n[#] No changes took place")
    else:
        print("\n[!] Error: Wrong input")

def show_table(s_table):
    curs=conn.cursor()
    curs.execute("SELECT * FROM "+s_table)
    item=curs.fetchall()
    if len(item)==0:
        print("\n[#] No values availabe (empty table)")
    else:
        fmt="double_grid"
        if s_table.upper()=="PATIENT":
            p_header=["Patient_ID", "First_Name", "Last_Name", "Patient_Age", "Date_of_Birth", "Sex", "Address", "Phone", "Insurance_ID", "Admission_Date"]
            print(tabulate(item, headers=p_header, tablefmt=fmt))
        elif s_table.upper()=="DOCTOR":
            doc_header=["Doctor_ID", "First_Name", "Last_Name", "Specialization", "Age", "Sex", "Address", "Phone"]
            print(tabulate(item, headers=doc_header, tablefmt=fmt))
        elif s_table.upper()=="DIAGNOSIS":
            diag_header=["Patient_ID", "Patient_Diagnosis", "Room_Number", "Treated_By"]
            print(tabulate(item, headers=diag_header, tablefmt=fmt))
        else:
            print("[!] Error: Wrong Table Name")

######################Abin Krishna###########################

######################Kishen#################################
#Put ur modified functions here (Inplace of this text)
######################Kishen#################################

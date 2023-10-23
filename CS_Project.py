import mysql.connector as sq
from getpass import getpass

def show_tables():
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    show_tables = cursor.fetchall()
    tables = []
    for i in show_tables:
        for z in i: #Due to the fact that returned list of tables in the form [(t1,),(t2,)]
            tables.append(z)
    for i in tables:
        print(f"{tables.index(i)+1} - {i}")

Datalist = []

try:
    print("\n\t\t\tEnter SQL Server Connection Details")
    print("_"*91)

    host = input("Host Name: ")
    user = input("User Name: ")
    db = input("Database Name: ")
    passwd = getpass("Database Connection Password: ") # By using "getpass" whenever u type the password it will be hidden in the terminal
    
    conn = sq.connect(host=host, username=user , database=db, passwd=passwd)

    if conn.is_connected():
        print("\nDatabase Connection Established!\n")
    print(f"-✧˖°. Welcome To The {db} Databse Interface ˖°.✧-\n")
    print("List of Tables-")
    show_tables()
    
    conn.close()

except sq.Error:
    print("\nConnection Failed!")
    print(sq.Error)
    print("Make sure you have entered the right credentials for the database connection\n")

def show_tables():
    conn_cursor = conn.cursor()
    conn_cursor.execute("SHOW TABLES")
    show_tables = conn_cursor.fetchall()
    tables = []
    for i in show_tables:
        for z in i: #Due to the fact that returned list of tables in the form [(t1,),(t2,)]
            tables.append(z)
    for i in tables:
        print(f"{tables.index(i)+1} - {i}")

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
Datalist = []

try:
    print("          Enter SQL Server Connection Details")
    print("__________________________________________________________ ")
    host = input("Host Name: ")
    user = input("User Name: ")
    Database = input("Database Name: ")
    passwd = input("Database Connection Password: ")
    conn = mysql.connector.connect(host=host, user=user , database=Database, passwd=passwd)
    if conn.is_connected():
        print("Database Connection Established!\n")
    print(f"-✧˖°. Welcome To The {Database} Databse Interface ˖°.✧-\n")
    print("List of Tables-")
    show_tables()
    
    conn.close()

except mysql.connector.Error:
    print("Connection Failed!")
    print(mysql.connector.Error)
    print("Make sure you have entered the right credentials for the database connection")

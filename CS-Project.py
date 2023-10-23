import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", Database= "", passwd = "")

conn.commit()
conn.close()

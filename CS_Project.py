import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", database="", passwd="")
cur = conn.cursor()

conn.commit()
conn.close()

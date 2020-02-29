import mysql.connector

DB = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="orszagok"
)

cursor = DB.cursor()
cursor.execute("SELECT * FROM orszagok WHERE nepesseg > 160000")
myResult = cursor.fetchall()

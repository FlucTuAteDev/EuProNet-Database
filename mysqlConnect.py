import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="orszagok"
)

cursor = db.cursor()
cursor.execute("SELECT * FROM orszagok WHERE nepesseg > 160000")
myResult = cursor.fetchall()
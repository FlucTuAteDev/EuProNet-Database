import mysql.connector

myDb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="orszagok"
)

myCursor = myDb.cursor()
myCursor.execute("SELECT * FROM orszagok WHERE nepesseg > 160000")
myResult = myCursor.fetchall()
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
)

cursor = db.cursor()
cursor.execute("SHOW DATABASES LIKE 'EUPRONET';")
result = cursor.fetchall()
if(len(result) > 0):
    print("DB exists already.")
else:
    print("Database doesn't exist yet. Creating...")
    with open("protodb.sql", encoding="utf-8") as f:
        sql = f.read()
    cursor.execute(sql)

db.database = "EUPRONET"
cursor = db.cursor()

#sql = "SELECT orszag, nepesseg FROM orszagok WHERE nepesseg > 160000 LIMIT 3"
#cursor.execute(sql)
#result = cursor.fetchall()
#for entry in result:
    #print(f"Entry: {entry}")
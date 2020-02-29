import mysql.connector

dbname = "EUPRONET"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
)

#Does the db exist already?
cursor = db.cursor()
cursor.execute(f"SHOW DATABASES LIKE '{dbname}';")
result = cursor.fetchall()
if(len(result) > 0):
    print("DB exists already.")
else:
    print("Database doesn't exist yet. Creating...")
    #Create from protodb.sql
    with open("protodb.sql", encoding="utf-8") as f:
        querycount = 0
        for sql in f.read().split(";"):
                if(querycount == 1): 
                    #set cursor once db is created
                    db.database = dbname
                    cursor = db.cursor()

                cursor.execute(sql)
                querycount += 1
    

db.database = dbname
cursor = db.cursor()

sql = "SELECT orszag, nepesseg FROM orszagok WHERE nepesseg > 160000 LIMIT 3"
cursor.execute(sql)
result = cursor.fetchall()
for entry in result:
    print(f"Entry: {entry}")
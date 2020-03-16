"""
File to sql: Uploads buffer file contents to database
"""

import mysql.connector
import argparse
import re
import os
from collections import namedtuple

dirname = os.path.dirname(__file__)
protodb = os.path.join(dirname, "protodb.sql")


fields = "host username password dbname filename" # exposed, configurable settings
Settings = namedtuple("Settings", fields, defaults=[None] * len(fields.split()))

default = Settings(
    username= "HU", 
    password= "GkHfm0Sm5OZ6keqX",
    host= "176.241.15.209",
    dbname= "EUPRONET"
)

#   READ SETTINGS FROM CONFIGURATION FILE

fromcfg = default._asdict()
try:    
    with open(os.path.join(dirname, "config.cfg"),"r", encoding="utf-8") as f:
        pattern = re.sub(r" ", "|", fields)
        for line in f.readlines():
            key, value =  [x.strip() for x in line.split("=", 1)]
            if(re.match(pattern, key)):
                fromcfg[key] = value
except:
    print("Config file doesn't exist or can't be read")

## USER INPUT

fromcfg = Settings(**fromcfg)
parser = argparse.ArgumentParser(description="Uploads buffer file contents to database")

parser.add_argument(
        "-f", "--filename", required= fromcfg.filename == None )
parser.add_argument(
        "-u", "--username", required= fromcfg.username == None )



config = fromcfg._asdict()
args = vars(parser.parse_args())
for k in args:
    if(args[k] != None):
        config[k] = args[k]
        
print(Settings(**config))

try:
    db = mysql.connector.connect(
    host = default.host,
    user = default.username,
    passwd = default.password,
    database = default.dbname
    )
except mysql.connector.errors.ProgrammingError as e:
    print(f"Error: Could not estabilish connection to {default.host} \n {e}")
    quit()

cursor = db.cursor()
# cursor.execute(f"SHOW DATABASES LIKE '{dbname}';")

cursor.execute(f"SELECT CURRENT_USER();")
result = cursor.fetchall()
print(result)
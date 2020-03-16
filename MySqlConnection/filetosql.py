"""
File to sql: Uploads buffer file contents to database
"""

import mysql.connector
import argparse
import re
from os import path
from collections import namedtuple

dirname = path.dirname(__file__)
#protodb = os.path.join(dirname, "protodb.sql")
CFGFILE = path.join(dirname, "config.cfg")

# exposed, configurable settings
fields = "address username password dbname filename logfile" 

Settings = namedtuple("Settings", fields, defaults=[None] * len(fields.split()))

default = Settings(
    username= "HU", 
    password= "GkHfm0Sm5OZ6keqX",
    address= "176.241.15.209",
    dbname= "EUPRONET"
)

#   1. Read settings from configuration file
cfg =  default._asdict()
try:    
    with open(CFGFILE,"r", encoding="utf-8") as f:
        pattern = '|'.join( [f"^{x}$" for x in fields.split()] )
        for line in f.readlines():
            try:
                key, value =  [x.strip() for x in line.split("=", 1)]
                if(re.match(pattern, key)):
                    cfg[key] = value
                else:
                    print(f"Warning: Unexpected setting '{key}'. It will be removed from the config file.")
            except ValueError :
                print(f"Setting '{line.strip()}' is not an assignment. It will be removed from the config file.")
except:
    print("Config file doesn't exist or could not be read")

# 2. Ask user for any settings missing

parser = argparse.ArgumentParser(description="Uploads buffer file contents to database")

arg = namedtuple("Argument", "short long req")
args = {
    "filename": arg("-f", "--filename", True),
    "username": arg("-u", "--username", True),
    "address":  arg("-a", "--address" , True),
    "password": arg("-p", "--password", True),
    "logfile":  arg("-l", "--logfile" , False)
}
    
for k, a in args.items():
    # prompt user if config file doesn't define a required value
    if(a.req):
        req = cfg[k] == None 
    parser.add_argument(a.short, a.long, required=req)

args = vars(parser.parse_args())
for k, v in args.items():
    if (v != None and v.strip() != ""):
        cfg[k] = v

# 3. Reconstruct config file

with open(CFGFILE, "w", encoding="utf-8") as f:
    for k, v in cfg.items():
        if (v != None and v.strip() != ""): 
            f.write(f"{k} = {v}\n")

cfg = Settings(**cfg)

try:
    db = mysql.connector.connect(
        host = cfg.address,
        user = cfg.username,
        passwd = cfg.password,
        database = cfg.dbname
    )
except mysql.connector.errors.ProgrammingError as e:
    print(f"Error: Could not estabilish connection to {cfg.address}: \n {e}")
    quit()

cursor = db.cursor()
# cursor.execute(f"SHOW DATABASES LIKE '{dbname}';")

cursor.execute(f"SELECT CURRENT_USER();")
result = cursor.fetchall()
print(result)
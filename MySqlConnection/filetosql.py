"""File to sql: Uploads buffer file contents to database"""

import mysql.connector
import argparse
import re
from os import path
from collections import namedtuple

####################################################
# exposed, configurable settings
fields = "address username password dbname filepath logfile" 
arg = namedtuple("Argument", "short long req")
args = {
    "filepath": arg("-f", "--filepath", True),
    "username": arg("-u", "--username", True),
    "address":  arg("-a", "--address" , True),
    "password": arg("-p", "--password", True),
    "logfile":  arg("-l", "--logfile" , False)
}
####################################################
Settings = namedtuple("Settings", fields, defaults=[None] * len(fields.split()))

default = Settings(
    username= "HU", 
    password= "GkHfm0Sm5OZ6keqX",
    address= "176.241.15.209",
    dbname= "EUPRONET"
)

dirname = path.dirname(__file__)
#protodb = os.path.join(dirname, "protodb.sql")

def GetFullPath(p, d = dirname):
    if path.isabs(p):
        return p
    else:
        return path.join(d,p)

CFGFILE = GetFullPath("config.cfg")



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

#4. Connect to database

try:
    db = mysql.connector.connect(
        host = cfg.address,
        user = cfg.username,
        passwd = cfg.password,
        database = cfg.dbname,
        connect_timeout = 3
    )
except Exception as e:
    print(f"Error: Could not estabilish connection to {cfg.address}: \n {e}")
    quit()

cursor = db.cursor()
# cursor.execute(f"SHOW DATABASES LIKE '{dbname}';")

filepath = GetFullPath(cfg.filepath)

history = []
unprocessed = []

#5. Read file contents to dictionary

sql = f"SELECT id FROM `countrycodes` WHERE code = '{cfg.username}' LIMIT 1"
cursor.execute(sql)
countrycode = cursor.fetchone()[0]
try:
    with open(filepath, "r") as f:
        for l in f.readlines():
            if l.strip() == "": continue
            keys = "country"
            vals = f"'{countrycode}'"
            try:
                for pair in l.split(";"):
                    k,v = [x.strip() for x in pair.split(":", 1) if x.strip() != ""]
                    keys = ", ".join((keys, k))
                    vals = ", ".join((vals, f" '{v}'"))
                history.append(l)
            except Exception as e:
                print(f"Could not parse line '{l.strip()}'. It will be left in the buffer file.") #\n\t {e}")
                unprocessed.append(l)
                continue
#6. Send query

            sql = f"INSERT INTO `queries` ({keys}) VALUES ({vals});"
            print(sql)
            cursor.execute(sql)
                    
except Exception as e:
    print(f"Could not read file at '{filepath}'{e}")
    db.close()
    quit()

db.commit()

with open(filepath, "w") as f:
    f.writelines(unprocessed)

if cfg.logfile != None:
    with open(GetFullPath(cfg.logfile), "a") as f:
        f.writelines(history)
        f.write("\n")
    
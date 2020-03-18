"""File to sql: Uploads buffer file contents to database"""

# region imports
import sys
import time
import mysql.connector
import argparse
import re
from os import path
from collections import namedtuple

# endregion

# region settings

# exposed, configurable settings
fields = "address username password dbname filepath logfile"
arg = namedtuple("Argument", "short long req")
args = {
    "filepath": arg("-f", "--filepath", True),
    "username": arg("-u", "--username", True),
    "address": arg("-a", "--address", True),
    "password": arg("-p", "--password", True),
    "logfile": arg("-l", "--logfile", False),
}
Settings = namedtuple("Settings", fields, defaults=[None] * len(fields.split()))

default = Settings(
    username="HU",
    password="GkHfm0Sm5OZ6keqX",
    address="176.241.15.209",
    dbname="EUPRONET",
)
# endregion

# region absolute paths
dirname = path.dirname(__file__)


def GetFullPath(p, d=dirname):
    if path.isabs(p):
        return p
    else:
        return path.join(d, p)


CFGFILE = GetFullPath("config.cfg")

# endregion

# region 1. Read settings from configuration file
cfg = default._asdict()
try:
    with open(CFGFILE, "r", encoding="utf-8") as f:
        pattern = "|".join([f"^{x}$" for x in fields.split()])
        for line in f.readlines():
            try:
                key, value = [x.strip() for x in line.split("=", 1)]
                if re.match(pattern, key):
                    cfg[key] = value
                else:
                    print(
                        f"Warning: Unexpected setting '{key}'. It will be removed from the config file."
                    )
            except ValueError:
                print(
                    f"Setting '{line.strip()}' is not an assignment. It will be removed from the config file."
                )
except:
    print("Config file doesn't exist or could not be read")

# endregion

# region 2. Ask user for any settings missing


parser = argparse.ArgumentParser(description="Uploads buffer file contents to database")


for k, a in args.items():
    # prompt user if config file doesn't define a required value
    if a.req:
        req = cfg[k] == None
    parser.add_argument(a.short, a.long, required=req)

args = vars(parser.parse_args())
for k, v in args.items():
    if v != None and v.strip() != "":
        cfg[k] = v

# endregion

# region 3. Reconstruct config file


with open(CFGFILE, "w", encoding="utf-8") as f:
    for k, v in cfg.items():
        if v != None and v.strip() != "":
            f.write(f"{k} = {v}\n")

cfg = Settings(**cfg)
# endregion

# region 4. Connect to database

try:
    db = mysql.connector.connect(
        host=cfg.address,
        user=cfg.username,
        passwd=cfg.password,
        database=cfg.dbname,
        connect_timeout=3,
    )
except Exception as e:
    print(f"Error: Could not estabilish connection to {cfg.address}: \n {e}")
    sys.exit()

cursor = db.cursor()
# endregion

# region 5. Get country code from username
filepath = GetFullPath(cfg.filepath)
if not path.isfile(filepath):
    print(f"Could not read file at '{filepath}''")
    db.close()
    sys.exit()

sql = f"SELECT id FROM `countrycodes` WHERE code = '{cfg.username}' LIMIT 1"
cursor.execute(sql)
countrycode = cursor.fetchone()[0]  # TODO: handle if this returns empty
# endregion

# region 6. Upload

unprocessed = set([])


def Upload():
    """ Reads file contents to dictionary
        Sends query
        Updates history and unprocessed
        Returns the  number of queries sent"""
    history = []

    with open(filepath, "r") as f:
        for l in f.readlines():
            if l.strip() == "" or l in unprocessed:
                continue
            keys = "country"
            vals = f"'{countrycode}'"
            try:
                for pair in l.split(";"):
                    k, v = [x.strip() for x in pair.split(":", 1) if x.strip() != ""]
                    keys = ", ".join((keys, k))
                    vals = ", ".join((vals, f" '{v}'"))
                history.append(l)
            except Exception as e:
                print(
                    f" Could not parse line '{l.strip()}'. It will be left in the buffer file."
                )  # \n\t {e}")
                unprocessed.add(l)
                continue
            # Send query

            sql = f"INSERT INTO `queries` ({keys}) VALUES ({vals});"
            # print(sql)
            try:
                cursor.execute(sql)
            except Exception as e:
                print(f"SQL Error: {e}")

    db.commit()

    with open(filepath, "w") as f:
        f.writelines(unprocessed)

    if history != [] and cfg.logfile != None:
        with open(GetFullPath(cfg.logfile), "a") as f:
            f.writelines(history)
            f.write("\n")

    return len(history)

# endregion

# region 7. Monitoring

print(
    f"Monitoring {cfg.filepath} [CTRL+C to exit] ..."
)  # TODO animate: Monitoring. .. ...
try:
    while True:
        sent = Upload()
        if sent:
            timestamp = time.strftime(r"%Y-%m-%d %H:%M:%S")
            print(f" {timestamp} - Sent {sent}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Monitoring ended")

# endregion

# region 8. Cleanup

db.close()

# endregion

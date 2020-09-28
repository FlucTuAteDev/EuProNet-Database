"""File to sql: Uploads buffer file contents to database"""

# region imports
import sys
import time
import argparse
import re
from os import path
from collections import namedtuple
import requests

# endregion

# region settings

# exposed, configurable settings
fields = "address username password filepath logfile"
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
    address="api.derimiksa.hu"
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

#TODO:  custom exceptions    
cfg = default._asdict()
try:
    with open(CFGFILE, "r", encoding="utf-8") as f:
        pattern = "|".join([f"^{x}$" for x in fields.split()]) # ^field$: exact match
        for line in f.readlines():
            try:
                key, value = [x.strip() for x in line.split("=", 1)]
                if re.match(pattern, key):
                    cfg[key] = value
                else:
                    print(f"Warning: Unexpected setting '{key}'. It will be removed from the config file.")
            except ValueError:
                print(
                    f"Setting '{line.strip()}' is not an assignment. It will be removed from the config file."
                )
except:
    print("Config file doesn't exist or could not be read")

# endregion

# region 2. Ask user for any settings missing
#TODO: arg to revert settings to default from cmd
#TODO: write to cfg even if not all of required settings are specified

parser = argparse.ArgumentParser(description="Uploads buffer file contents to database")


for k, a in args.items():
    # prompt user if config file doesn't define a required value
    req = False
    if a.req:
        c = cfg[k]
        req = c == None or c.strip() == "" #empty or unspecified
    parser.add_argument(a.short, a.long, required=req)

args = vars(parser.parse_args())
for k, v in args.items():
    if v != None and v.strip() != "":
        cfg[k] = v

# endregion

# region 3. Reconstruct config file

def NotEmptyOrNone(value: v):
    return v != None and v.strip() != ""

with open(CFGFILE, "w", encoding="utf-8") as f:
    for k, v in cfg.items():
        if NotEmptyOrNone(v):
            f.write(f"{k} = {v}\n")

cfg = Settings(**cfg)
# endregion

# region 4. Connect to database

# Login and get token
url = f"{cfg.address}/login"
print(f"Logging in as {cfg.username} at {cfg.address} ...")
try:
    login = requests.post(url, json={"username": cfg.username, "password": cfg.password}).json()

    # Check stat
    if login["status"] == "ok":
        token = login["token"]
    else:
        print(f" Login failed: {login['msg']}")
        sys.exit()

except Exception as e:
    print(f"Could not establish connection to {url}: \n {e}")
    sys.exit()
print(" Login successful!")

# region 5. Check if file exists and get country code
filepath = GetFullPath(cfg.filepath)
if not path.isfile(filepath):
    print(f"Could not read file at '{filepath}'")
    db.close()
    sys.exit()

# region 6. Upload

# TODO: check if keys given are real column names
# TODO: check if given state values exist
# TODO: correct excused formatting mistakes when writing to history (e.g. ;;;)

unprocessed = []

def Upload():
    """ Reads file contents to dictionary
        Sends query
        Updates 'history' and 'unprocessed'
        Returns the  number of queries sent"""
    global unprocessed
    history = []

    with open(filepath, "r+") as f:
        lines = f.readlines()
        f.truncate(0)
        for l in lines:
            lstr = l.strip()
            if lstr == "" or lstr in [upl.strip() for upl in unprocessed]: continue
            data = {"token": token}
            try:
                for pair in l.split(";"):
                    if(pair.strip() == ""): continue
                    #seperate at the first ':'; remove unneeded whitespace; ignore empty assignments
                    k, v = [x.strip() for x in pair.split(":", 1) if x.strip() != ""]
                    data[k] = v
            except: # Exception as e:
                print(f" Could not parse line {l!r}. It will be left in the buffer file.")  # \n\t {e}")
                unprocessed.append(lstr)
                continue
            # print(data)
            
            # Send query
            try:
                insert = requests.post(f"{cfg.address}/insert/print", json=data).json()
                
                if insert["status"] == "ok":
                    print(f" Upload successful: {'; '.join(f'{k}: {v}' for k, v in data.items() if k != 'token')}")
                else:
                    print(f"Data insertion failed: {insert['msg']}")
            except Exception as e:
                print(f"Incorrect upload data: \n {e}")
                
            history.append(l)

    unprocessed = [l for l in unprocessed if l in lines]
    with open(filepath, "a") as f:
        f.write("\n".join(unprocessed))

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
            timestamp = time.strftime(r"%H:%M:%S")
            print(f" {timestamp} - Sent {sent}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Monitoring ended")

# endregion

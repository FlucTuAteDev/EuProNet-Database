path = "ardudata.txt"
print(f"File: {path}")
try:
     with open(path, "x"):
        print("\tFile doesn't exist, creating...")
except:
    print("\topening...")

with open(path,"r+") as f:
    if(f.readable()):
        print(f"File content:\n {f.readlines()}" )
    else:
        print:"File could not be read."

    print("haloka", file=f)
    f.seek(0)
    print(f"File content after writing:\n {f.readlines()}" )

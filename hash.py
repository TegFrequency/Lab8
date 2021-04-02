import os
import time
import hashlib


def main():#Check for existing hash file
    if os.path.exists("/tmp/hashes.csv") != True:
        #Hash file does not exist
        print("Hash file does not exist. Will create a current hash file.")
        makehash("hashes.csv")
    else:
        #Hash file exists
        print("Hash file exists. Will generate a current hash file and compare.")
        makehash("currenthashes.csv")
        compare("hashes.csv", "currenthashes.csv")
    return

def makehash(fname):
    nohash = ["/dev", "/proc", "/run", "/sys", "/tmp", "/var/lib", "/var/run", "/vmlinuz.old", "/vmlinuz", "/swapfile"]
    #reference bogotobogo.com/pthon/python_traversing_directory_tree_recursively_os_walk.php
    filename = "/tmp/"+fname
    files = open(filename, "w")
    for base, dirnames, fnames in os.walk("/home/tegtmeyer/labs"):
        for f in fnames:
            fullpath = os.path.join(base, f)
            if fullpath in nohash:
                continue
            hashing = hashlib.sha256()
            with open(fullpath, 'rb') as scratchwork:
                hold = scratchwork.read(1000)
                while len(hold) > 0:
                    hashing.update(hold)
                    hold = scratchwork.read(1000)
                filehash = hashing.hexdigest()
            t = os.stat(fullpath)
            date = time.ctime(t.st_atime)
            files.write("Filename: "+ fullpath + ", Hash: "+filehash+ ", Date/Time: "+ date +"\n")
    files.close()
    return

def compare(originalhash, currenthash):
    check = open("/tmp/changes.txt", "w")
    file1 = "/tmp/"+originalhash
    file2 = "/tmp/"+currenthash
    with open(file1, "r") as original:
        with open(file2, "r") as current:
            hashes =[]
            for line in original:
                line = line.strip("\n")
                name, hashed, date = line.split(",")
                hashed = hashed.strip("Hash: ")
                hashed = hashed.strip()
                hashes.append(hashed)
            for info in current:
                info = info.strip("\n")
                name2, hashed2, date2 = info.split(",")
                hashed2 = hashed2.strip("Hash: ")
                hashed2 = hashed2.strip()
                if hashed2 not in hashes:
                    #Something changed
                    check.write(name2+ ", Hash: "+hashed2+ ", "+date2 +"\n")
    check.close()
    return

main()


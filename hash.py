import hashlib
with open('adminDB.txt','r') as f:
    for line in f:
        line = line.strip()
        num = line.split(":")[0]

        hashnum = hashlib.md5(num.encode())
        hashnum = hashnum.hexdigest()

        with open('HashAdminDB.txt','a') as f2:
            f2.write(hashnum + "\n")
            print("%s :has been written" % hashnum)
            f2.close()
    f.close()

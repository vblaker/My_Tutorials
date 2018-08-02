import hashlib
import os

fnamelst = os.listdir(os.getcwd())
print(fnamelst)

def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()

for file in fnamelst:
    print('File: {}, MD5: {}'.format(file, md5sum(file)))

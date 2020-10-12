import os
import hashlib

dirpath = 'E:/'
dirs = os.listdir(dirpath)
# for file in dirs:
#     print(os.path.join(dirpath, file))

for root, dirs, files in os.walk(dirpath):
    for name in files:
        with open(os.path.join(root, name), 'rb') as fp:
            data = fp.read()
        file_md5 = hashlib.md5(data).hexdigest()
        print(os.path.join(root, name)+'\t'+file_md5)
    for name in dirs:
        print(os.path.join(root, name))

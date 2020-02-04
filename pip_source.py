#!/usr/bin/python
# coding: utf-8

import platform
import os

os_type = platform.system()
if "Linux" == os_type:
    fileDirPath = "%s/.pip" % os.path.expanduser('~')
    filePath = "%s/pip.conf" % fileDirPath
    if not os.path.isdir(fileDirPath):
        os.mkdir(fileDirPath)
    fo = open(filePath, "w")
    fo.write(
        "[global]\nindex-url=http://mirrors.aliyun.com/pypi/simple/\n"
        "[install]\ntrusted-host=mirrors.aliyun.com\n"
    )
    fo.close()
    print("Configuration is complete")
elif "Windows" == os_type:
    fileDirPath = "%s\\pip" % os.path.expanduser('~')
    filePath = "%s\\pip.ini" % fileDirPath
    if not os.path.isdir(fileDirPath):
        os.mkdir(fileDirPath)
    fo = open(filePath, "w")
    fo.write(
        "[global]\nindex-url=http://mirrors.aliyun.com/pypi/simple/\n"
        "[install]\ntrusted-host=mirrors.aliyun.com\n")
    fo.close()
    print("Configuration is complete")
else:
    exit("Your platform is unknow!")

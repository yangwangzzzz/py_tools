# coding=utf-8
__author__ = 'Administrator'
import os
import hashlib
import sys
import json

reload(sys)
sys.setdefaultencoding("utf-8")

d = {}
def get_path(path):
    f_list = os.listdir(path)
    for name in f_list:
        fullname = os.path.join(path, name)
        if os.path.isdir(fullname):
            get_path(fullname)
        else:
            d[fullname] = md5sum(fullname)

def sumfile(fobj):
    m = hashlib.md5()
    while True:
        d = fobj.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()


def md5sum(fname):
    if fname == '-':
        ret = sumfile(sys.stdin)
    else:
        try:
            f = file(fname, 'rb')
        except:
            return 'Failed to open file'
        ret = sumfile(f)
        f.close()
    print fname, ret
    return ret

get_path('./')
s = json.dumps(d)
f = open('path.json', 'w')
f.write(s)
f.close()

# coding=utf-8
__author__ = 'Administrator'
import os
import ftplib

host_addr = '127.0.0.1'
username = 'ywz'
password = ''

asset_url = 'E:/pycode/'
file_list = ['0.jpg', 'py_t/banana.jpg', 'py_t/.idea/misc.xml']

ftp = ftplib.FTP()
print 'start connect %s' % host_addr
ftp.connect('127.0.0.1', 21)
print 'connect success %s' % host_addr
print 'start login %s' % host_addr
ftp.login(username, password)
print 'login success %s' % host_addr

def upload(f_name, rname):
    f_name = asset_url + f_name
    file_handler = open(f_name, 'rb')
    ftp.storbinary('STOR %s' % rname, file_handler)
    file_handler.close()
    print u'已传送: %s' % f_name

for file_name in file_list:
    ftp.cwd('')
    if (file_name.rfind('/')) != -1:
        dir_name = file_name[:file_name.rfind('/')]
        ff_name = file_name[file_name.rfind('/') + 1:]
        try:
            ftp.mkd(dir_name)
            ftp.cwd(dir_name)
            print u'创建目录 %s' % dir_name
            upload(file_name, ff_name)
        except:
            ftp.cwd(dir_name)
            upload(file_name, ff_name)
    else:
        upload(file_name, file_name)
        pass



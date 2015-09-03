# coding=utf-8
__author__ = "yangwangzheng"

import pysvn
import os
import ftplib
import datetime
import re

revision_file_name = 'revision.txt'

svn_username = 'test'
svn_password = 'test'
svn_url = 'htpps://127.0.0.1/svn/test'

asset_url = 'asset/'

ftp_url = '127.0.0.1'
ftp_remote_dir = 'test'
ftp_username = 'test'
ftp_password = 'test'

g_revision_begin = 0

def get_revision():
    if os.path.exists(revision_file_name):
        with open(revision_file_name, 'r') as f:
            revision = int(f.readline())
    else:
        revision = int(raw_input('input svn revision:'))
    return revision;

def save_revision(revision):
    with open(revision_file_name, 'w') as f:
        f.write(str(revision))
    print u'保存本次更新的版本号 %s' % revision

def get_login(realm, user, may_save):
    return True, svn_username, svn_password, False

# 获得两个svn版本号里的差异文件列表
def get_diff_list():
    diff_list = []
    global g_revision_begin
	
    g_revision_begin = get_revision()
	
    revision_min = pysvn.Revision(pysvn.opt_revision_kind.number, g_revision_begin)
    revision_max = pysvn.Revision(pysvn.opt_revision_kind.head)
	
    client = pysvn.Client()
    client.callback_get_login = get_login
	
    log = client.log(svn_url)
    g_revision_begin = log[0].revision.number
	
    summary = client.diff_summarize(svn_url, revision_min, svn_url, revision_max)
	
    for changed in summary:
        if changed['summarize_kind'] == pysvn.diff_summarize_kind.added or changed['summarize_kind'] == pysvn.diff_summarize_kind.modified:
            diff_list.append(changed['path'])

    return diff_list


# 过滤中文名文件
def has_hz(text):
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    return zhPattern.search(text)

def upload(path):
    path = asset_url + path
    f = open(path, 'rb')
    try:
        ftp.storbinary('STOR %s' % os.path.basename(path), f)
    except Exception as error:
        print error
    f.close()
    print 'send: %s' % path

def upload_list(diff_list):
    ftp.cwd(ftp_remote_dir)
    for name in diff_list:
        if not os.path.exists(asset_url + name):
            print u'本地不存在 %s' % name
            continue
        if not os.path.isfile(asset_url + name):
            continue
        if has_hz(asset_url + name):
            continue
        if (name.rfind('/')) != -1:
            dir_name = name[:name.rfind('/')]
            try:
                ftp.mkd(dir_name)
                print u'创建新目录 %s' % dir_name
            except:
                pass
            ftp.cwd(dir_name)
            upload(name)
            for i in range(len(dir_name.split('/'))):
                ftp.cwd('..')
        else:
             upload(name)
    ftp.quit()

def modify_index_html():
    pass

if __name__ == '__main__':
    d_list = get_diff_list()
    if len(d_list):
        ftp = ftplib.FTP()
        ftp.connect(ftp_url, 21, 60)
        ftp.login(ftp_username, ftp_password)
        upload_list(d_list)
        modify_index_html()
        save_revision(g_revision_begin)
    else:
        print u'没有文件需要更新'

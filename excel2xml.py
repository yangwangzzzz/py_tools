# coding=utf-8
__author__ = 'yangwangzzzz'
import xlrd
import sys
import os
import codecs
import types

reload(sys)
sys.setdefaultencoding("utf-8")

def get_xml_path(path):
    return path.split('.')[0] + '.xml'

def convert_encode(data):
    if type(data) is types.UnicodeType:
        data = data.encode('utf-8')
    elif type(data) is types.FloatType:
        data = int(data)
    return data

def sheet2xml(sheet, xmlfile):
    f = codecs.open(xmlfile, 'w', 'utf-8')
    f.write(u'<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write(u'<%s>\n' % sheet.name)

    for row in range(1, sheet.nrows):
        s = u'<item '
        tmp = [u'%s="%s"' % (str(convert_encode(sheet.cell_value(0, col))), str(convert_encode(sheet.cell_value(row, col)))) for col in range(sheet.ncols)]
        s += u' '.join(map(str, tmp))
        s += u'/>\n'
        f.write(s)
    f.write(u'</%s>' % sheet.name)

def convert2xml(path):
    workbook = xlrd.open_workbook(path)
    for sheet in workbook.sheets():
        if sheet.ncols != 0:
            xmlfile = sheet.name + '.xml'
            sheet2xml(sheet, xmlfile)

def convert_dir():
    lists = os.listdir('.')
    for name in lists:
        if os.path.isfile(name):
            if name.rfind('.xlsx') != -1 or name.rfind('.xls') != -1:
                convert2xml(name)

if __name__ == '__main__':
    convert_dir()

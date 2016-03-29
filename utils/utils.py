#!/usr/bin/env python
# coding=utf-8
# author: b0lu
# mail: b0lu@163.com
from fileinput import filename
import json, os, subprocess, tempfile
from GLog import elog,getDlog

def get_request(brequests):
    request = ""
    for b in brequests:
        request += chr(b) 
    return request

def write_file(filename, data):
    f = open(filename, 'w')
    print "#"*50
    print f
    print "the filename is =>"+filename
    print "#"*50
    try:
        f.write(data)
    except Exception,e:
        elog.exception(e)
    finally:
        f.close()
        
def delFile(filename):
    if os.path.exists(filename) and os.path.isfile(filename):
        os.remove(filename)
    
def pexec(*args):
    return subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0].rstrip()


def makeTempfile(content):
    temp = tempfile.TemporaryFile()
    try:
        temp.write(content)
        temp.seek(0)
    except Exception,e:
        elog.exception(e)
    finally:
        return temp
 
if __name__ == '__main__':
    write_file("/tmp/proxyscan/xx.log", "test")

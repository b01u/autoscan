#!/usr/bin/env python
# coding=utf-8
# author: b0lu
# mail: b0lu@163.com
from sys import path
from os.path import dirname, abspath
path.append( dirname(dirname(abspath(__file__))) )
from utils.utils import makeTempfile, write_file, delFile
from utils.GLog import elog, getDlog
from config.config import cf
from utils.DBMysql import gm
from fuzzle.scanIssue import scanIssue
from fuzzle import vulTypes
import time, os, re, datetime
#import subprocess
from gevent import subprocess

class sqlmapAudit(object):
    def __init__(self, drequest):
        self.dreq = drequest
        self.dlog = getDlog(__name__)
        self.filename = cf.sqlmap_tmppath+str(time.time())
        self.insertVul = lambda scanissue: gm.insertVul(scanissue)
        
    def audit(self):
        try:
            print "the tmp filename is :"+ self.filename
            write_file(self.filename, self.dreq.request)
            slow_cmd = "python sqlmap.py -r %s --dbms=Mysql --batch"%self.filename
            quick_cmd = "python sqlmap.py -r %s --dbms=Mysql --smart  --batch"%self.filename
            cmd = slow_cmd if len(self.dreq.url) < 150 else quick_cmd
            result = self.psqlmap(cmd)
            m = re.search(r"Place[\w\W]+Parameter[\w\W]+Payload", result, re.IGNORECASE)
            if m:
                method = re.findall(r"Place:(.*)", result, re.IGNORECASE)[0].strip()
                parameter = re.findall(r"Parameter:(.*)", result, re.IGNORECASE)[0].strip()
                payload = '\r\n'.join(re.findall(r"Payload:(.*)", result, re.IGNORECASE))
                self.dlog.debug("[ SqlmapAudit Vul Result ] method: %s, parameter: %s, payload: %s"%(method, parameter, payload))
                vul = scanIssue(rid=self.dreq.rid, type= vulTypes.sql, host= self.dreq.host, url= self.dreq.url, method=method, parameters=parameter, payload= payload)
                self.insertVul(vul)
        except Exception,e:
            elog.exception(e)
        finally:
            #delFile(self.filename)
            pass
        
    def psqlmap(self, cmd):
        print "sqlmap cmd :" + cmd
        print "sqlmap path:" + cf.sqlmap_path
        start = time.time()
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd= cf.sqlmap_path, bufsize=10000, close_fds=True)
        #p = subprocess.Popen(cmd,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd= cf.sqlmap_path, bufsize=100000, close_fds=True)
        '''
        while p.poll() is None:
            time.sleep(1)
            now = datetime.datetime.now()
            print "the sqlmap is running time :"+str((now-start).seconds)+"\tthe poll status is =>"+str(p.poll())
            if (now - start).seconds > 60*5:
                try:
                    p.terminate()
                    p.kill()
                except Exception,e:
                    elog.exception(e)
                    return ""
                return ""
            output, unused_err = p.communicate()
            print output[:1000]
            if p.stdin:
                p.stdin.close()
            if p.stdout:
                p.stdout.close()
            if p.stderr:
                p.stderr.close()
            try:
                p.kill()
            except OSError:
                pass
            return output
        '''
        output, unused_err = p.communicate()
        retcode = p.poll()
        if retcode:
            raise subprocess.CalledProcessError(retcode, cmd, output=output)

        print "sqlmap runing time=>"+str(time.time()-start)
        return output
        
def getPluginClass():
    return sqlmapAudit 

def ptsqlmap(self, cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd= cf.sqlmap_path)
    output, unused_err = p.communicate()
    retcode = p.poll()
    if retcode:
        raise subprocess.CalledProcessError(retcode, cmd, output=output)
    return output

if __name__ == "__main__":
    from utils.GRedis import gredis
    from fuzzle.grequest import DRequest
    req = gredis.getTask()
    dreq = DRequest(req)
    csqlmap = sqlmapAudit(dreq)
    csqlmap.audit()
    

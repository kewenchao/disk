import logging
import pymysql
import os
import web
import subprocess
from rest_framework.response import Response
from rest_framework import status

urls = (  
    '/disk33/(.*)', 'DiskUsage'  
)  
  
app = web.application(urls, globals())  
  
class DiskUsage:
    def GET(self, name):
        try:
            num = self.connect_mysql(name)
            if num:
                path = "Z:\\26\\COF_API_STORAGE\\project\\"+str(num)
                data = self.get_json_data(path)
                obj = self.get_data(data)
                return {name : obj}
            else:
                return "Please fill in the correct user name "
        except Exception as e:
            return {'err_msg': e}


    def get_json_data(self, path):
        cmd = "Get-ChildItem -Recurse | Measure-Object -Sum Length"
        args=[r"powershell.exe", cmd]
        p=subprocess.Popen(args, stdout=subprocess.PIPE, cwd=path)
        dt=p.stdout.readlines()
        return dt


    def bytes2human(self, n):
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.1f%s' % (value,s)
        return '%sB' % n

    def get_data(self, data):
        d = {}
        for i in data:
            m = i.decode('utf-8','ignore').strip('\r\n')
            x = m.split(":")
            if x[0].__contains__("Sum"):
                v = self.bytes2human(int(x[1]))
        return str(v)
        

    def connect_mysql(self, name):
        conn = pymysql.connect(
            host="10.239.44.26",
            user="root",
            password="mysql",
            database="CofluentDB",
            charset="utf8")
        cursor = conn.cursor()
        sql = "SELECT * FROM cofluentdb.tb_users where username='%s'"%(name)
        cursor.execute(sql)
        ret = cursor.fetchone()
        num = ret[0] if ret else ''   
        cursor.close()
        conn.close()
        return num

if __name__ == "__main__": 
    app.run()

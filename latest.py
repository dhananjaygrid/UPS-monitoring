import schedule

import time
from easysnmp import Session
import MySQLdb
from datetime import datetime
import threading
oidsapc = ['.1.3.6.1.4.1.318.1.1.1.2.2.3.0', '.1.3.6.1.4.1.318.1.1.1.12.1.1.0', '.1.3.6.1.4.1.318.1.1.1.4.2.3.0']
# 1.3.6.1.4.1.318.1.1.1.12.1(outlet status) .1.3.6.1.4.1.318.1.1.1.4.2.3.0(power)
oideaton = ['1.3.6.1.2.1.33.1.2.3.0']#,1.3.6.1.2.1.33.1.4.4.1.4.1minutes(integer), outlet,power
def some_func(ip = ''):
	class Job(threading.Thread):
	    def __init__(self, ip, conn, sleepBuffer=0):
		threading.Thread.__init__(self)
		    
		 
		
		   
		self.ip = ip
		#print self.ip
		self.conn = conn
		self.sleepBuffer = sleepBuffer
	    def run(self):
		
		    
		self.session = Session(hostname=self.ip, community='public',version=1,timeout=1,retries=1)
		self.job(self.ip)

	    def job(self, ip):
		if ip == '192.168.184.100':   
		    #print "HEYYY im the loop"     
		    descriptions = self.session.get(oideaton)
		    t = int(descriptions[0].value)
		    seconds = t * 60
		    remTime = time.strftime("%H:%M:%S", time.gmtime(seconds))            
		    #print("Rem_time for %s: %s" % (ip, remTime))
		else : 
		    #description = self.session.get('.1.3.6.1.4.1.318.1.1.1.2.2.3.0')
		    descriptions = self.session.get(oidsapc)
		    t = int(descriptions[0].value)
		    seconds = t / 100
		    minutes = seconds / 60
		    T = datetime.now().strftime('%H:%M:%S')
		
		    remTime = time.strftime("%H:%M:%S", time.gmtime(seconds))
		    outstat = int(descriptions[1].value)
		    pow = descriptions[2].value
		    #print ("timeofprobe for %s: %s" % (ip, T))
		    #print("Rem_time for %s: %s" % (ip, remTime))
		    #print ("Outlet status is %s" %(outstat))
		    #print("Power is %s" %(pow))
		    cur = self.conn.cursor()
		    cur.execute("update UPS set time_of_probe = '%s' where ip = '%s'" % (T,ip))
		    self.conn.commit()
		    cur.execute("update UPS set rem_time = '%s' where ip = '%s'" % (remTime,ip))
		    self.conn.commit()
		    cur.execute("update LOW_PRIORITY UPS set out_stat = '%s' where ip = '%s'" % (outstat, ip))
		    self.conn.commit()
		    cur.execute("update LOW_PRIORITY UPS set out_power = '%s' where ip = '%s'" % (pow, ip))
		    self.conn.commit()
		    sleepTime = 0
		    nextProbeTime = 0
		    if minutes > 90: 
		        nextProbeTime = 1800 
		    elif minutes > 60:
		        nextProbeTime = 1200
		    elif minutes > 30:
		        nextProbeTime = 600
		    elif minutes > 10:
		        nextProbeTime = 180
		    elif minutes > 5:
		        nextProbeTime = 120
		    elif minutes > 2:
		        nextProbeTime = 30
		    print("nextProbeTime for %s: %s" % (ip, nextProbeTime))
		    probetime = time.strftime("%H:%M:%S", time.gmtime(int(nextProbeTime)))
		    cur.execute("update LOW_PRIORITY UPS set nex_probe = '%s' where ip = '%s'" % (probetime, ip))
		    self.conn.commit()
		    time.sleep(nextProbeTime)
		    time.sleep(self.sleepBuffer)
		
		    if seconds > 59:
		    
		        self.job(ip)
		    else:
		        print('stopped')  
		    
	db  = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="parameters")
	cur = db.cursor()
        if ip == '':
            cur.execute("select ip from UPS")
        else:
            
	    cur.execute("select ip from UPS where ip = %s" %(ip))
	rows = cur.fetchall()
        #print rows
	#session = Session(hostname='192.168.184.27', community='public', version=2)
	#description = session.get(SNMPv2-MIB::sysDescr.0)

	threads = []
	for row in rows:
	    conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="parameters")
	    
	    time.sleep(1)
	    thread = Job(row[0], conn)
	    thread.start()
	    
	    threads.append(thread)
	for thread in threads:
	    thread.join()

some_func()

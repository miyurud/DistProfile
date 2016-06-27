'''
Created on 14 Mar, 2014

@author: miyuru
'''

import SocketServer
import socket
import time
import commands
import os
import sys
import threading
import thread
import ConfigParser

workdir = ''
localdir = ''
exitFlag = False
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
curhostname = ''
exitFlag = False

def init(argv):
	global workdir
	global localdir
	global curhostname
#         workdir = config.get("Main", "workdir")
#         localdir = config.get("Main", "localdir")
	curhostname = commands.getoutput('hostname')
	curhostname = curhostname[:curhostname.find('.')]

def runWorker(argv):
        global server
	global workdir

	init(argv)

        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ##server.setsockopt(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 2830))

        server.listen(5)

        ##-->monitor_thread = threading.Thread(target=monitor)
        ##-->monitor_thread.setDaemon(True)
        ##-->monitor_thread.start()		
		
        while exitFlag == False:
                (sock, address) = server.accept()
                if exitFlag == True:
			#sock.send("q\n")
			#sock.shutdown(socket.SHUT_RDWR)
			#sock.close()
			server.close();
			break;
				
                thread = Worker(sock)
                thread.setDaemon(1)
                thread.start()

	print 'exitting...'

class Worker(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        global exitFlag

	self.sock.send('send');

        while exitFlag == False:
            data = self.sock.recv(1024).strip()

            if data == 'alive':
    		self.sock.send('yes');
            elif data == 'cmd-no-out':
                self.sock.send('send');
                command_to_exec = self.sock.recv(1024).strip()
                #print '>' + command_to_exec + '<'
                commands.getoutput(command_to_exec)
    	    elif data == 'cmd':
    		self.sock.send('send');
    		command_to_exec = self.sock.recv(1024).strip()
                #print '>' + command_to_exec + '<'
                command_out = commands.getoutput(command_to_exec)
                #print '|' + str(command_out) + '|'
                lines = command_out.split('\n')               
                length = len(lines) 
                count = 0
                outstr = ''
                while count < length:
                  outstr += lines[count] + '|'
                  count += 1
              
                #print str(outstr)

   		self.sock.send(outstr)
                self.sock.send('\n')
            elif data == 'shtdn':#Shutdown the entire worker
		exitFlag = True
                sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sk.connect(('127.0.0.1', 2830))#just connect to the local worker instance so that it will automatically shutdown since we have set the flag
                break
	    elif data == 'close': #Just close this session
		break
    	    elif data == 'clear':
    		if os.path.isdir(localdir) == True:
    			command = "rm -rf " + localdir + "/*"
    			os.system(command)
    		self.sock.send('cleared')
        self.sock.close()
	sys.exit(2)

def getNumberLines(filePath):
	numlines = 0
	for line in open(filePath):
		if line != '\n':
			numlines += 1
	return numlines

def getOutputLineCount(resultdir):
	command = "ls " + resultdir + '/*'
	output = commands.getoutput(command)
	lines = output.split('\n');
	totalLineCount = 0

	length = len(lines)
	count = 0

	if output.find('No such file or directory') != -1:
		return 0

	while count < length:
		if lines[count].find('startjob') != -1:
			count += 1
			continue

		totalLineCount += getNumberLines(lines[count])
		count += 1
	
	return totalLineCount

runWorker(sys.argv[1:])

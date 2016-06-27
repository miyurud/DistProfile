'''
Created on 14 Mar, 2014

@author: miyuru
'''

import sys
import os
import commands
import time
import getpass
import thread

from Nmon import *
from Consts import *

#hostList = ["169.254.1.9", "169.254.1.10", "169.254.1.12", "169.254.1.13"] # For the moment we assume that we have only these 4 hosts
hostList = ["155.69.146.42"]
username = ''
password = ''
#dist_profiler_install_dir = "/home/miyuru/software/DistProfiler"
dist_profiler_install_dir = "/home/miyuru/workspace-python/DistProfile"

def usage():
    print '#########################################################################'
    print 'DistProfile - Run multiple profilers simultaneously, in distributed hosts'
    print '#########################################################################'
    print '\r\nDistProfile.py [comma separated host list] <sessiondir> <exp time> <nmon_record_window>'
    print 'issue \'exit\' on console to exit.\r\n'
    print 'Example : python DistProfile.py [169.254.1.9,169.254.1.10,169.254.1.12,169.254.1.13] /home/miyuru/projects/pamstream/experiments/test1 7:30 15'

def cleanUpExistingWorkers():
    for host in hostList:
        print str(host)
        shutdownWorker(host)
        
def setupWorkers():
    for host in hostList:
          cd = os.getcwd()
          #command = 'python ' + dist_profiler_install_dir + '/Worker.py &'
          #command = 'mkdir /tmp/ttest123'
          command = dist_profiler_install_dir + '/runworker.sh &'
          #commands.getoutput(command)
          #output = os.system("python " + cd + "/sshclient.py " + host  + " '" + command + "' " + username + " " + password)
          cmd = "python " + cd + "/sshclient.py " + host  + " '" + command + "' " + username + " " + password
          thread.start_new_thread(setupWorker, (cmd,))
#This function is almost similar to the previous one. But this is the one that actually sets up the Worker.
def setupWorker(command):
    os.system(command)

def getseconds(timestr):
    pos=timestr.find(':')

    if(pos == -1):
        return timestr
    else:
        minutes = int(timestr[0:pos])
        seconds = int(timestr[pos + 1:])
        return seconds + (minutes * 60)

def main(argv):
    global username
    global password
    global hostList
    
    if len(sys.argv) < 5:
       usage()
       sys.exit(2)
    else:
       hosts = argv[0]
       
       print '|'+str(hosts)+'|'
       
       hosts = hosts[1:len(hosts) - 1]
       hostList = hosts.split(',')
       sessiondir = argv[1].strip()
       exptime = argv[2]
       recordWindow = int(argv[3])
       totalNumberofRecordings = getseconds(exptime)/recordWindow
       
       print 'host list : ' + str(hostList)
       print 'session dir : ' + str(sessiondir)
       print 'experiment time : ' + str(exptime)
       print 'record window : ' + str(recordWindow)
       print 'total number of recordings : ' + str(totalNumberofRecordings)
           
       username = 'miyuru'
       password = getpass.getpass(str(username) + "'s Password: ")
    
       cleanUpExistingWorkers()
       print 'Done cleanUpExistingWorkers'
       time.sleep(5) #Wait 2 seconds till the things get stabilized
       setupWorkers()
       print 'Done setupWorkers'
       time.sleep(8) #Wait 2 seconds till the things get stabilized
       stopNmons(hostList)
       time.sleep(2)
       print 'Done stop nmons'
       #Next we run the nmons
       runNmons(hostList, recordWindow, totalNumberofRecordings, sessiondir)
       print 'Done runNmons'
       x = None
       print 'Enter \'exit\' to close.' 
       sys.stdout.write('> ')
       while True:
            x = raw_input()
            if x == 'exit':
                print 'Getting ready to shutdown (wait till stabilize)...'
                #time.sleep(recordWindow)
                time.sleep(2)
                print 'Stabilized.'
                print 'Shutting down the daemons...'
                stopNmons(hostList)
                #stop_oprofile(hostsList)
                cleanUpExistingWorkers()
                print 'Now exitting...'
                sys.exit(0)
main(sys.argv[1:])

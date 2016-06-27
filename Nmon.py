'''
Created on 15 Mar, 2014

@author: miyuru
'''
import time
import datetime

from WorkerInterface import *

nomon_app = '/home/miyuru/software/nmon/nmon_x86_64_ubuntu13'

def runNmons(hostList, recordWindow, totalNumberofRecordings, cursessiondir):
    host_len = len(hostList)
    for host in hostList:
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
        command = nomon_app + ' -f -s ' + str(recordWindow) + ' -c ' + str(totalNumberofRecordings) + ' -F ' + cursessiondir + '/out-' + str(host_len) + '-' + host + '-' + st +'.nmon'
        print 'nmon command |' + str(command) + '|'
        #sendCommandWithoutReturn(host, command)
        #thread.start_new_thread(run_sparate_thread, (host, command,))
        print str(host) + "-->" + str(command)
        sendCommandWithReturn(host, command)

   
def stopNmons(hostList):
    result = ''
    for host in hostList:
        command = 'ps -u miyuru | grep nmon'
        result = sendCommandWithReturn(host, command)
        print 'result |' + str(result) + '|'
        if result.find('?') != -1:
                psid = result.split('?')[0].strip()
                print 'ps id is : ' + str(psid)
                command = 'kill ' + psid
                print 'Stopping nmon on : ' + host
                result += sendCommandWithReturn(host, command)
        
    print 'Final result |' + str(result) + '|' 
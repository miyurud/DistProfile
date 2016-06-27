'''
Created on 15 Mar, 2014

@author: miyuru
'''

import socket
import errno

from Consts import *

def sendCommandWithReturn(host, cmd):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, Consts.PORT))
    
    #By defualt we receive 'send'
    received = sock.recv(1024).strip()
    if received != 'send':
        return 'Error connecting to host ' + str(host)
    
    sock.send('cmd')
    received = sock.recv(1024).strip()
    if received != 'send':
        return 'Error connecting to host ' + str(host)    
    
    sock.send(cmd)
    
    received = sock.recv(1024).strip()
    
    return received

def sendCommandWithoutReturn(host, cmd): # Here we do not expect a return value from the remote process. Specially good for situations where the remote process blocks infinitely.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, Consts.PORT))
    
    #By defualt we receive 'send'
    received = sock.recv(1024).strip()
    if received != 'send':
        return 'Error connecting to host ' + str(host)
    
    sock.send('cmd-no-out')
    received = sock.recv(1024).strip()
    if received != 'send':
        return 'Error connecting to host ' + str(host)    
    
    sock.send(cmd)

def shutdownWorker(host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, Consts.PORT))
    except:
        return
    #By defualt we receive 'send'
    received = sock.recv(1024).strip()
    if received != 'send':
        return 'Error connecting to host ' + str(host)
    
    sock.send('shtdn')
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 21:55:20 2017

@author: Matheus Inoue
"""

import socket
 
HOST = '192.168.25.60'   # Enter IP or Hostname of your server
PORT = 12345    # Pick an open Port (1000+ recommended), must match the server port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
 
#Lets loop awaiting for your input
while True:
    command = input('Enter your command: ')
    
    #s.send(command)
    s.send(command.encode('utf-8'))
    reply = s.recv(1024)
    if reply == b'Terminating':
        break
    print (reply)
    
    
    
  
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 13:48:45 2018

@author: shikhanair
"""

# Import socket module
import socket               
 
# Create a socket object
conn = socket.socket()         
 
# Define the port on which you want to connect
port = 3650               
 
# connect to the server on local computer
conn.connect(('127.0.0.1', port))
 
# receive data from the server
print(conn.recv(1024))
# close the connection
conn.close()       

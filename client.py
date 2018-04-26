#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 13:48:45 2018

@author: shikhanair
"""
import socket
import sys

def main():
	
	# Define connection port
	port = 5100

	# Check for args
	if(len(sys.argv) < 2):
		print("No host specified\n")

	host = sys.argv[1]

	if(len(sys.argv) == 3):
		port = int(sys.argv[2])

	# Create the socket
	conn = socket.socket()

	# Connect to the server at the specified host
	conn.connect((host, port))

	# Receive data from the server.
	mssg = conn.recv(64).decode()
	print(mssg)

	# Close the connection
	conn.close()

if __name__ == "__main__":
	main()

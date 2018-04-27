#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 13:48:45 2018

@author: shikhanair
"""
import socket
import sys
import ssl

def main():
	
	# Define the default connection port and host
	port = 5100
	host = 'localhost'

	# Check for args
	if(len(sys.argv) >= 2):
		host = sys.argv[1]

	if(len(sys.argv) == 3):
		port = int(sys.argv[2])

	# Create SSL Context
	context = ssl.SSLContext()
	context.verify_mode=ssl.CERT_REQUIRED
	context.check_hostname=True
	#context.load_default_certs(ssl.Purpose.SERVER_AUTH)
	context.load_verify_locations("certfile.crt")

	# Create a normal socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Wrap socket in SSL context
	conn = context.wrap_socket(s, server_hostname="Swapnair")

	# Connect to the server at the specified host
	conn.connect((host, port))

	print("Server Validated: Communication Initiated")

	while True:
		
		cmd = input("Enter a command: \n")

		if(cmd == 'GET'):
			conn.send(cmd.encode())
		elif(cmd == 'POST'):
			conn.send(cmd.encode())
		elif(cmd == 'END'):
			conn.send(cmd.encode())
			break
		else:
			print("Error: No command entered!")



	# Close the connection
	conn.close()

if __name__ == "__main__":
	main()

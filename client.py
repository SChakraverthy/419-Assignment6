#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assignment 5 OpenSSL Message Board: server.py
Swapna Chakraverthy, Shikha Nair
"""
import socket
import sys
import ssl
import pickle

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
		
			# Send the GET command to the server.
			conn.send(cmd.encode())

			# Ask the user for the group name argument.
			grp = input("Enter group name: ")

			# Send the length of the argument to the server.
			numbytes_sent = str(len(pickle.dumps(grp)))
			conn.send(numbytes_sent.encode())

			# Send the group name to the server.
			conn.sendall(pickle.dumps(grp))

			# Receive the length of the pickled messages list.
			num_bytes = int(conn.recv().decode())

			# Receive the list of messages from the server.
			data = conn.recv(num_bytes)
			msgs = pickle.loads(data)

			for m in msgs:
				print(m)

		
		elif(cmd == 'POST'):

			# Send the POST command to the server.
			conn.send(cmd.encode())

			# Ask the user for the group name and the message.
			grp = input("Enter group name: \n")
			mssg = input("Enter message: \n")

			params = (grp, mssg)

			# Send the length of the pickled data to the server.
			numbytes_sent = str(len(pickle.dumps(params)))

			try:
				conn.send(numbytes_sent.encode())
			except ssl.SSLError as e:
				print(e)
				break
			
			# Send the data to the server
			try:
				conn.sendall(pickle.dumps(params))
			except ssl.SSLError as e:
				print(e)
				break

		elif(cmd == 'END'):
			conn.send(cmd.encode())
			break
		else:
			print("Error: No command entered!")



	# Close the connection
	conn.close()

if __name__ == "__main__":
	main()

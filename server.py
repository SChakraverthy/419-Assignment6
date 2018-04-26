# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import socket

def main():
	port = 5100
	
	#Create the socket and bind it to the defined port.
	conn = socket.socket()
	conn.bind(('', port))

	#Listen for connections
	conn.listen(10)
	print('Listening for connections...')

	while True:
		
		# Accept incoming connections
		(c, addr) = conn.accept()
		print('Connection accepted from: ', addr)

		mssg = 'Connected to the server!'.encode()
		c.send(mssg)
		c.close()
		break

	conn.close()

if __name__ == "__main__":
	main()
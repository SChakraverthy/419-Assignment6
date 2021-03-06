# -*- coding: utf-8 -*-
"""
Assignment 5 OpenSSL Message Board: server.py
Swapna Chakraverthy, Shikha Nair
"""
import socket
import hashlib
import ssl
import pickle
import re
import time
import datetime
import sys



#Turns Message Board name in a file-friendly name for the Message Board file
def fileFriendly(name):
    return re.sub(r'\W+', '', name)
	
# This function takes a group name (grpname) and a message (msg) as arguments
# Converts the group name into a file friendly format and then opens or creates
# a file to append the new message to. The message is added with a timestamp.
def post(grpname, msg):
    
    grp = fileFriendly(grpname)
    
    with open(grp+".p", "ab") as mb:
        nmsg = msg + " " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        #print("posting: ", nmsg)
        pickle.dump(nmsg, mb)
    
    return 

# This function takes a group name (grpname) as an argument.
# It converts the group name to a file friendly format and opens the file with that name.
# It retrieves a list of messages from the file and returns it.
def get(grpname):
	
	msgs = []
	grp = fileFriendly(grpname)

	with(open(grp+".p", "rb")) as mb:
		while True:
			try:
				msgs.append(pickle.load(mb))
			except EOFError:
				break

	return msgs
	

#this function takes the username and password provided by the client and verifies the login information
#True if login success, False otherwise
#If the username exists and the salted and hashed password is the same as what's in the file, returns True
#If the username doesn't exist in the file, function adds username and salted and hashed password, returns True
#If the username exists but the salted and hashed password doesn't match, returns False
def login(un, pw):
    
    hpw = hashlib.pbkdf2_hmac('sha256', pw.encode('utf-8'), b'salt', 100000)
    
    
    with open("logininfo.txt") as f:
      
        
        #Check for username in file
        for line in f:
            info = line.split()
            #if line has username
            if info[0] == un:
                #if password hash matches
                if info[1] == hpw:
                    print("Login Successful")
                    return True
                print("Incorrect Password")
                return False
        
        f.write(un + " " + hpw)
        print("New User Added!")
        

    return True

# This function takes the ssl-wrapped connection socket as an argument.
# It runs on a loop and receives client commands: GET, POST, and END. GET: Receives the group name argument from 
# the client and calls the get() function to retrieve a list of messages. It then sends the list of messages to The
# client. POST: Receives the group name and message arguments from the client and calls the post() function to
# add the message and/or group to the board. END: Receives no arguments from the client. Ends the server's acceptance of
# commands from the client.
def handleconn(conn):
	
	while True:
		
		cmd = conn.recv(5).decode()

		if(cmd == "GET"):

			# Receive the number of bytes to expect from the client.
			num_bytes = int(conn.recv().decode())

			# Receive the group name argument from the client.
			data = conn.recv(num_bytes)
			grp = pickle.loads(data)

			# Provide the group name as argument to the get function.
			# Receive a list of messages in return.
			msgs = get(grp)
			
			# Send the length of the pickled messages list to the client.
			numbytes_sent = str(len(pickle.dumps(msgs)))
			conn.send(numbytes_sent.encode())

			# Send the messages to the client.
			conn.sendall(pickle.dumps(msgs))


		elif(cmd == "POST"):
			
			# Receive the number of bytes to expect from the client.
			num_bytes = int(conn.recv().decode())

			# Receive the data from the client
			data = conn.recv(num_bytes)
			grp, mssg = pickle.loads(data)

			post(grp, mssg)

		elif(cmd =="END"):
			break
		else:
			print("No valid commands received")
			continue




def main():
	port = 5100
	
	# Create the SSL Context
	context = ssl.SSLContext()
	context.check_hostname=False
	context.load_cert_chain(certfile="certfile.crt", keyfile="keyfile.key")

	#Create the socket and bind it to the defined port.
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('', port))

	#Listen for connections
	s.listen(10)
	print('Listening for connections...')

	while True:
		
		# Accept incoming connections
		(c, addr) = s.accept()
		print('Connection accepted from: ', addr)

		# Wrap the normal socket.
		try:
			conn = context.wrap_socket(c, server_side=True)
		except ssl.SSLError as e:
			print("wrap_socket Error: ", e)
			s.close()
			c.close()
			return

		handleconn(conn)

		c.close()
		break

	s.close()

if __name__ == "__main__":
	main()

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


#Turns Message Board name in a file-friendly name for the Message Board file
def fileFriendly(name):
    return re.sub(r'\W+', '', name)


def post(grpname, msg):
    
    grp = fileFriendly(grpname)
    
    with open(grp+".p", "wb") as mb:
        nmsg = msg + " " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        pickle.dump(nmsg, mb)
    
    return 

def get(grpname):
    
    grp = fileFriendly(grpname)
    
    with open(grp+".p", "rb") as mb:
        msgs = pickle.load(mb)
        
        #NEED TO SEND msgs TO CLIENT!!!
        #For now:
        print(msgs)
    
    return

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

def handleconn(conn):
	
	while True:
		
		cmd = conn.recv(5).decode()

		if(cmd == "GET"):
			print("Received GET command from client!")
		elif(cmd == "POST"):
			print("Received POST command from client!")
		elif(cmd =="END"):
			print("Received END command from client!")
			break
		else:
			print("No valid commands received")




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

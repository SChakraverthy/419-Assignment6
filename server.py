# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import socket
import hashlib

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

#!/usr/bin/python

import socket
import sys
import os

def Main():
	# Create TCP/IP socket	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Get IP address of the computer node
	serveripAdd = socket.gethostname()
	#print socket.gethostbyname(serveripAdd)
	port = 9999
	serverAdd = ('',port)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# Bind the socket and listen for incoming connections.	
	s.bind(serverAdd)
	s.listen(5)
	print "Running Server..."

	while True:
		c, addr = s.accept()						#Accept incoming connection
		option = c.recv(1024)						#recieve user option
	
		if option == "1":							#Receive clien's option
			GET(c)
		elif option == "2":
			SEND(c)
		else:
			print "Error in receiving option!"
			return
	s.close()

def SEND(c):
	filename = c.recv(1024)
	if os.path.isfile(filename):					#check if file exists
		c.send(str(os.path.getsize(filename)))		# if yes, send file size
		with open(filename, 'rb') as f:				# Send file 
			bytesToSend = f.read(1024)
			c.send(bytesToSend)
			while bytesToSend != "":
				bytesToSend = f.read(1024)
				c.send(bytesToSend)
		print "File sent!"
	else:
		c.send("0");								# If No, Send filesize as 0 to client

	c.close()										# close the socket
		
def GET(c):
	filename = c.recv(1024)							# Receive file name
	data = c.recv(1024)								# Receive file size as string
	filesize = long(data)							# Convert to interger
	if filesize == 0:								# Check if file exists
		print "File does not exists"
		return
	else:
		print "Receiving a file from Client"		# If yes, receive file
		f = open('fromClient_'+filename,'wb')				# Open a new file and write data
		data = c.recv(1024)
		totalrecv = len(data)
		f.write(data)
		while totalrecv < filesize:					# Write all data
			data = c.recv(1024)
			totalrecv += len(data)
			f.write(data)
		print "Receive Complete"
		f.close()									# Close the file
	c.close()										# Close socket

if __name__ == '__main__':
	Main()		

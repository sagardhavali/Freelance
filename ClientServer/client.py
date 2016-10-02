#!/usr/bin/python

import socket
import sys
import os

def Main():
	# Get IP address from command line	
	print "Server IP Address: " + "<" + sys.argv[1] + ">"
	ipAdd = sys.argv[1]
	port = 9999

	# Create a TCP/IP socket	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to Server
	serverAdd = (ipAdd,port)
	s.connect(serverAdd)

	# Ask user for operation
	print "1. Send a file to Server"
	print "2. Receive a file from Sever"
	option = raw_input("Choose your option: ")
	
	if option=="1":
		s.send(option)								#Notify the server	
		SEND(s)
	elif option=="2":
		s.send(option)								#Notify the server	
		GET(s)
	else:
		print "Wrong Selection!"
		return
	s.close()

def SEND(s):
	filename = raw_input("Enter	the filename: ")	#Ask user for file name
	s.send(filename)								# send file name
	if os.path.isfile(filename):					# Check if file exists
		print "Sending a file to Server"
		size = str(os.path.getsize(filename))
		s.send(size)								# if yes, send file size
		with open(filename,'rb') as f:
			bytesToSend = f.read(1024)
			s.send(bytesToSend)
			while bytesToSend != "":
				bytesToSend = f.read(1024)
				s.send(bytesToSend)
		print "File sent!"
	else:
		s.send("0")									# If No, Send file as 0.
	
	s.close()										# Close the socket	
		
def GET(s):	
	filename = raw_input("Enter the filename: ")	#Ask user for file name
	s.send(filename)								#send file name	
	data = s.recv(1024) 							#receive file size. It is received as string
	filesize = long(data)							#convert to integer
	
	if filesize == 0:								#check if file exists
		print "File does not exists"
		return
	else:
		print "Receiving a file from Server..."		
		f = open('fromServer_'+filename, 'wb') 			#open a new file to write received data
		data = s.recv(1024)							#First chunk of data
		totalRecv = len(data)						#Length of first chunk of data.
		f.write(data) 								#write data to new file
		while totalRecv < filesize:					#Write all data
			data = s.recv(1024)
			totalRecv += len(data)
			f.write(data)
		print "Receive Complete"
		f.close()									#close the file
	s.close()										#close socket
	
if __name__ == '__main__':
	Main()

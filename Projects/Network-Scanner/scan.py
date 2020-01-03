'''
MTPROJECTS
Last Modified: January 3, 2020
Description: Simple network scanner. Enter your file locations and path before running the script.
Script is not perfect and was quickly coded. There are many more modifications that can be done. Feel free to clone the project,
and make your modifications. 
'''

import socket
import nmap
import os
from pathlib import Path

print("\n\nProgram Starting\n-------------------------------------------")
print("Port scanner object created")
nm = nmap.PortScanner()

print("Verifying IP file. If file exists, open, else create new file")
File_object = open(r"ENTER FILE LOCATION", "a+") #Enter file location

pathfile = Path(r"ENTER FILE LOCATION") #Path to check if file is empty

print("Scanning network for host IP Addresses")
nm.scan(hosts='192.168.0.1/24', arguments='-sP') #enter IP range to scan (subnet)

listOfIPS = []


#Will verify if the file is empty or not and redirect to appropriate function
def verifyIPList(File_object):

	if pathfile.stat().st_size == 0:
		print("File is empty")
		emptyFileIPList()
		readFromFile()
		getHostNameAndState()

	else:
		print("File contains IP Addresses")
		readFromFile()
		checkFileIPList()


#Function will copy all ip addresses for scan to text file
def emptyFileIPList():

	print("[Initially file empty] Opening file")
	print("Copying IP Addresses to file")

	for hosts in nm.all_hosts():
		hoststr = hosts + "\n"
		File_object.write(hoststr)
		print("Copied host: ", hosts, " \n")

	File_object.close()
	print("Closing file")


#Function will compare IP from text file with scan results 	
def checkFileIPList():
	
	print("Veryifying for new host IP Addresses")

	for newhosts in nm.all_hosts():
		if newhosts not in listOfIPS:
			print("New IP Address found: ", newhosts)
			addIPToList(newhosts)
			listOfIPS.append(newhosts)
		else:
			continue
	getHostNameAndState()


#Reads IPS from text file
def readFromFile():

	File_object = open(r"ENTER FILE LOCATION", "r") #open file to read
	fileLines = File_object.readlines()
	for lines in fileLines:
		lineread = lines.replace("\n", "")
		listOfIPS.append(lineread)

	File_object.close()


#Function will add new IPs to the text file
def addIPToList(NewIP):

	print("Adding new IP Address to file")
	File_object = open(r"ENTER FILE LOCATION", "a+")
	hoststr = NewIP + "\n"
	File_object.write(hoststr)
	File_object.close()


#Get all host names by ID and state of hosts
def getHostNameAndState():
	
	print("\nList of Hosts in your network\n---------------------------------------------------------------------------")
	count = 0
	uphosts = 0
	downhosts = 0 

	for hostIP in listOfIPS:
		
		try:
			hoststate = nm[hostIP].state()
			uphosts = uphosts + 1	
		except:
			hoststate = "down"
			downhosts = downhosts + 1

		try:
			hostname = socket.gethostbyaddr(hostIP)

		except:
			hostname = ('No Host Name',)


		#print("Host IP: ",hostIP, "   State: ", hoststate, " Host Name: ", hostname[0])
		linetoprint = ('{:<2} {:<20} {:<2} {:<10} {:<2} {:<25}'.format('Host IP:',hostIP,'State:',hoststate,'Host Name:',hostname[0]))
		print(linetoprint)
		
		count = count + 1
	
	print('\nTotal Hosts Up:',uphosts, '\nTotal Hosts Down:',downhosts, '\nTotal Hosts:',count)


	
print("Verifying if file contains list of IP Addresses")
verifyIPList(File_object)

#''.format('test')
# print("Host names:")










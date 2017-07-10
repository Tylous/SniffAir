#!/usr/bin/python
import sys
import os
from ConfigParser import SafeConfigParser
from Sniffer import *
from Connect2DB import *


def main():
	print "###################Place Holder for Main Menu#######################"
	print "###############################TO DO################################"
	print "-Ensure we create a function to install depencies"
	print "-Create/Update Actions to do the proper thing"
	print "-Creating testing functions"
	print "For testing purpoes make sure the airodump-ng is running with wlan0"
	print "Right now both Create and Load will just launch the Sniffing function"
	print "####################################################################"
	print "\n"                       
	print "1. Create a New Project"
	print "2. Load an Existing Project"
	print "3. Be lame and exit"

	ACTION = raw_input("What would you like to do: ")

	if ACTION in ["Create"]:
		db_name()
		create_connection()
		Load_Menu()
	elif ACTION in ["Load"]:
		db_name()
		print "something to go here"
	elif ACTION in ["Exit"]:
			sys.exit(0)
	else:
		print ("Error Try again")
		main()


def Load_Menu():
	print "###################Place Holder for Main Menu#######################"
	print "\n"                        
	print "1. LOAD new files"
	print "2. Do a LIVE capture"
	print "3. Work on an EXISTING info"
	print "4. Go Back to the previous menu"

	ACTION = raw_input("What would you like to do: ")

	if ACTION in ["Load"]:
		path = str(raw_input("Enter the full path: "))
		c = packet_sniffer()
		c.file(path)
	elif ACTION in ["Live"]:
		interface = str(raw_input("Enter the interface you wish to use: "))
		c = packet_sniffer()
		c.live_capture(interface)
		c.Signal(interface)
	elif ACTION in ["Existing"]:
		print "not invented yet"
	elif ACTION in ["Exit"]:
			main()
	else:
		print ("Error Try again")
		Load_Menu()


if __name__ == '__main__': 
	main()




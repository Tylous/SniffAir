#!/usr/bin/python
import sys
import os
from ConfigParser import SafeConfigParser
from Sniffer import *

def main():
	print "###################Place Holder for Main Menu#######################"
	print "###############################TO DO################################"
	print "-Ensure we create a function to install depencies"
	print "-Create/Update Actions to do the proper thing"
	print "-Create DB"
	print "-Creating testing functions"
	print "For testing purpoes make sure the airodump-ng is running with wlan0"
	print "Right now both Create and Load will just launch the Sniffing function"
	print "####################################################################"
	print "\n"
	print "What would you like to do:"                          
	print "1. Create a New Project"
	print "2. Load an Existing Project"
	print "3. Be lame and exit"

	ACTION = raw_input("What would you like to do: ")

	if ACTION in ["Create"]:
		c = packet_sniffer()
		c.run()
	elif ACTION in ["Load"]:
		c = packet_sniffer()
		c.run()
	elif ACTION in ["Exit"]:
			sys.exit(0)
	else:
		print ("Error Try again")
		main()

if __name__ == '__main__': 
	main()

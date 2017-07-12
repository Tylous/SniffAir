#!/usr/bin/python

#################################################
"""
Custom filters can be added by adding a function
to the the packet_sniffer class. Please note
in order for the filter to work you must add
it to the appropriate Layer Check. Follow the
syntax below. A module will be created down 
the road to automate this.
"""
#################################################

#from main import *
#from Connect2DB import *
#import Connect2DB
#import subprocess
import sys
import time
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
#import sqlite3
#from sqlite3 import Error


def Sniffer(pkt):

	if pkt.type == 0 and pkt.subtype == 8 : 
		if pkt.haslayer(Dot11Elt):
			try:
		#	try:
				if pkt[Dot11Elt:3]:
					CHL = str(ord(pkt[Dot11Elt:3].info))
					print CHL 
			except TypeError:
				CHL = pkt[Dot11Common].Ch_Freq 
				print CHL


		#	Sig = str(pkt[Dot11Common].Antsignal)
		#	print Sig
sniff(offline="/root/Downloads/RJdenverDay1-20160331-11-53-53-1.pcapdump", count=0, prn=Sniffer)

print "This shows up tntohing happen"

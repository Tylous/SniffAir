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
	if pkt.haslayer(Dot11):
		if pkt.type == 0 and pkt.subtype == 8 :
			SIG = pkt[Dot11Common].Antsignal
			print SIG


#sniff(iface='wlan0', count=15, prn=Sniffer)



		#	Sig = str(pkt[Dot11Common].Antsignal)
		#	print Sig
sniff(offline="/root/eap-02.cap", count=0, prn=Sniffer)

print "This shows up tntohing happen"


from main import *
from Connect2DB import *
import Connect2DB
import subprocess
import sys
import time
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import sqlite3
from sqlite3 import Error

class packet_sniffer():

	def __int__(self):
		super(Sniffer, self).__init__()

	def __getitem__(self, key):
		return key

	def file(self):
		interface = " "
		sniff(offline="/root/Kismet-20170512-12-03-53-1.pcapdump", count=0 ,prn=self.Sniffer)
		print "[+] Completed"
		

	def Sniffer(self, pkt):
		if pkt.haslayer(Dot11):
			if pkt.type == 0 and pkt.subtype == 8 : 
				self.Signal(pkt, interface)

			

	def Signal(self, pkt, interface):
		global SIG
		#if interface is not None:
		SIG = pkt[Dot11Common].Antsignal
		print SIG

		#else:
		#	SIG = str(pkt.dBm_AntSignal)





c = packet_sniffer()
c.file()

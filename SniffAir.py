#!/usr/bin/python
#from __future__ import print_function
import argparse
import sys
import thread
import time
from prettytable import PrettyTable
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import colorama
#from getch import getch, pause
import threading

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--Interface', metavar='interface', dest='interface', action='store', help='The Interface\n', required=False)
parser.add_argument('-s', '--SSID', metavar='ssid', dest='ssid', action='store', help='The SSID to attack\n', required=False)
parser.add_argument('-U', '--Usernames', dest='Usernames', action='store_true', help='List all Usernames Connected to the SSID\n', required=False)
parser.add_argument('-c', '--Channel', dest='channel', action='store_true', help='Set a specific Channel to listen on. If not set, will perform channel hoping\n', required=False)
parser.add_argument('-C', '--Clients', dest='clients', action='store_true', help='List all Clients Connected to the SSID\n', required=False)
parser.add_argument('-B', '--BSSID', dest='BSSID', action='store_true', help='Show all assocated BSSIDs\n', required=False)
parser.add_argument('-p', '--PCAP', dest='PCAP', action='store', help='Read a PCAP file. Must specific the path\n', required=False)
parser.add_argument('-w', '--Write', dest='WRITE', action='store_true', help='Write all Packets to a file\n', required=False)
args = parser.parse_args()

AUTHID = {}
USERID = []
BSSID = []
ap_list = []
BSSID_LIST = []
AUTHID_LIST = []
ESSID= []
ESSID_LIST= []
Channel= []
test= []
SSID= []
AP = args.ssid
station= []
APS= []
stations2= []
user= []
ssid= []
channel= []
def main():

	def Wifi(pkt):
	  global AUTHID
	  global USERID
	  global MADDRESS
	  global BSSID
	  global ESSID	
	  global AUTHID_LIST
	  global Channel
	  global test
	  global SSID
	  global APS
	  global station
	  global stations2
	  global AP
	  global user
	  global ssid
	  global test

##AP's mac address and Channel
	  types = (0, 2, 4)
	  if bool(args.BSSID):
	   if pkt.haslayer(Dot11):
	       if pkt.type == 0 and pkt.subtype == 8 :  
	          if pkt[Dot11Elt][0].info == AP:
	           if pkt.addr2 not in ap_list :
	                ap_list.append(pkt.addr2)
	                APS=str(ap_list)[1:-1].replace(',','\n')
	               	Channel.append(int(ord(pkt[Dot11Elt:3].info)))
	      
	#Client mac
	  if bool(args.clients):
	 	if pkt.haslayer(Dot11):
	     	 if pkt.type == 0 and pkt.subtype in types:
	        	hwaddr = pkt[Dot11].addr2
	        	ssid = pkt[Dot11Elt][0].info 
	        	if hwaddr not in station:
	        	 if ssid == AP:
	        		station.append(hwaddr)	
	        		stations2=str(station)[1:-1].replace(',','\n')

	  if bool(args.Usernames):
		  if pkt.haslayer(EAP):
			#if pkt[EAP].type ==1 :
				if len(pkt[EAP].identity) > 0:
			 		AUTHID=pkt[EAP].identity
					if AUTHID not in AUTHID_LIST:
						AUTHID_LIST.append(AUTHID)
						user=str(AUTHID_LIST)[1:-1].replace(',','\n')
	if bool(args.PCAP):
 	 sniff(offline=args.PCAP, prn=Wifi)
	else:
	 sniff(iface=args.interface, count=0, prn=Wifi)



thread.start_new_thread(main,())

#def test():
	  #key = getch()
	  #try:
	  #if key == "q":
	   # 	sys.exit(0)
	  #elif key == "r":
	   #     print "resume"
	        #test()
	  #elif key == "p":
	   #     print "pause"
	        #test()
	  #elif key == "d":
	   #     print "deauth"
	        #test()	        
    #else:
	 #       pass
	  #except KeyboardInterrupt:
	    #sys.exit(0)

def table():
  global AUTHID
  global USERID
  global MADDRESS
  global BSSID
  global ESSID	
  global AUTHID_LIST
  global channel
  global test
  global SSID
  global APS
  global station
  global stations2
  global AP
  global user
  global ssid
 
  title = []
  row = []


  if bool(args.BSSID):
	 title.append("BSSID")
	 row.append(str(APS)[1:-1].replace(',','\n'))
	 title.append("Channel")
	 row.append(str(Channel)[1:-1].replace(',','\n'))
  if bool(args.clients):
	 title.append("Client's MAC")
	 row.append(str(stations2)[1:-1].replace(',','\n'))
  if bool(args.Usernames):
	title.append("Usernames")
	row.append(user)
  
  print "SSID: " + str(AP)
  x = PrettyTable(title)
  x.add_row(row)
  print x
  #test()



def display():
	
	colorama.init()
	def put_cursor(x,y):
	    print "\x1b[{};{}H".format(y+1,x+1)

	def clear():
	    print "\x1b[2J"
	clear()
	put_cursor(0,0)
	count= 2
	while count > 1:
	 count +=1
	 table()
	 #test()
	 time.sleep(1)
	 put_cursor(0,0)
if __name__ == '__main__':
	display()

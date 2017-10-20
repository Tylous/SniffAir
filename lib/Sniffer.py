#!/usr/bin/python

from SniffAir import *
from Connect2DB import *
import Connect2DB
import subprocess
import sys
import os
import signal
import time
import logging
logging.getLogger("scapy.runtime").setLevel(logging.CRITICAL)
from scapy.all import *
import sqlite3
from sqlite3 import Error
import threading

load_contrib('ppi_cace')


GRN = '\033[92m'
BLU = '\033[34m'
RD = '\033[91m'
NRM = '\033[0m'


class packet_sniffer():
	def __int__(self):
		super(Sniffer, self).__init__()

	def __getitem__(self, key):
		return key

	def file(self, path):
		global sw
		sw = '2'
		print BLU + "[*]" + NRM + " Importing " + path
		sniff(offline=path, count=0 , store=0, prn=self.Sniffer)
		print "\n" + GRN + "[+]"+ NRM +" Completed"

	def live_capture(self, interface, band):
		global sw
		sw = '1'
		if band == "2.4":
			bd = "bg"
		elif band == "5.5":
			bd = "a"
		elif band == "both":
			bd = "abg"
		os.system('sudo screen -S sniff -d -m airodump-ng '+ interface +' --band '+ bd)
		print GRN + "[+]"+ NRM +" Sniffing... to monitor it yourself, open a new terminal and run: screen -r"
		while interface:
			try:
				sniff(iface=interface, count=0 , store=0, prn=self.Sniffer)
			except OSError:
				os.system('sudo screen -S sniff -X quit')
				print "\n" + RD + "[+]"+ NRM +" Network interface went down"
				break
			except socket.error:
				continue
			except KeyboardInterrupt:
				time.sleep(2)
				os.system('sudo screen -S sniff -X quit')
				print "\n" + GRN + "[+]"+ NRM +" Completed"
				break
			break

	def Sniffer(self, pkt):
		global connection
		sql = load()
		connect_db()
		if pkt.haslayer(Dot11):
			if pkt.type == 0 and pkt.subtype == 8 : 
				self.Vendor(pkt)
				self.MAC(pkt)
				self.SSID(pkt)
				self.Channel(pkt)
				self.Signal(pkt)
				self.ENC(pkt)
				sql.insert_ACCESS_POINT(SSID, MAC, Vendor, CHL, SIG, ENC, CHR, ATH)
			
			elif pkt.type == 0 and pkt.subtype == 4 : 
				self.MAC(pkt)
				self.SSID(pkt)
				self.Signal(pkt)
				self.Vendor(pkt)
				sql.Insert_Probe_REQUEST(SSID, MAC, Vendor, SIG)

			elif pkt.type == 0 and pkt.subtype == 5 : 
				self.MAC(pkt)
				self.SSID(pkt)
				self.Channel(pkt)
				self.Signal(pkt)
				self.ENC(pkt)
				self.Vendor(pkt)
				self.Resp_Probe_Client_Mac(pkt)
				sql.Insert_Probe_RESPONSE(SSID, MAC, Vendor, CHL, SIG, ENC, CHR, ATH, RPCM)
			
		if pkt.haslayer(EAP):
			if pkt[EAP].id == 1 and pkt[EAP].code == 2:
				try:
					if len(pkt[EAP].identity) > 0:
						self.EAP_Identity(pkt)
						sql.Insert_EAP(sender, user, ap)
				except TypeError:
					print "\n" + RD + "[+]"+ NRM +" An error has occurred"
					print pkt.show()
					os.kill(os.getpid(), signal.SIGINT)
 		

	def Vendor(self, pkt):
		global Vendor
		SC = pkt.addr2[0:8].upper()	
		Vendor = subprocess.check_output("grep "+ SC +" /usr/share/wireshark/manuf | cut -d\"#\" -f2", shell=True).rstrip('\n').lstrip().replace(","," ")
		if Vendor == "":
			Vendor = "Unknown"

	def Resp_Probe_Client_Mac(self, pkt):
		global RPCM
		RPCM = pkt.addr1

	def SSID(self, pkt):
		global SSID
		if str(pkt[Dot11Elt:1].info) == "":
			SSID="Hidden"
		elif str(pkt[Dot11Elt:1].info).startswith("\000"):
			SSID="Hidden" 
		else:
			SSID = str(pkt[Dot11Elt:1].info)


	def MAC(self, pkt):
		global MAC
		MAC = pkt.addr2

	def Channel(self, pkt):
		global CHL
		chanDict = {'5180': '36', '5190': '38', '5200': '40', '5210': '42', '5220': '44', '5230': '46', '5240': '48', '5250': '50', '5260': '52', '5270': '54', '5280': '56', '5290': '58', '5300': '60', '5310': '62', '5320': '64', '5500': '100', '5510': '102', '5520': '104', '5530': '106', '5540': '108', '5550': '110', '5560': '112', '5570': '114', '5580': '116', '5590': '118', '5600': '120', '5610': '122', '5620': '124', '5630': '126', '5640': '128', '5660': '132', '5670': '134', '5680': '136', '5690': '138', '5700': '140', '5710': '142', '5720': '144', '5745': '149', '5755': '151', '5765': '153', '5775': '155', '5785': '157', '5795': '159', '5805': '161', '5825': '165'}
		if pkt.haslayer(Dot11Elt):
			try:
				if pkt[Dot11Elt:3]:
					CHL = str(ord(pkt[Dot11Elt:3].info)) 
			except TypeError:
				CHL = str(pkt[Dot11Common].Ch_Freq)
				if CHL in chanDict:
					CHL = chanDict[CHL]
				else:
					print "ERROR"

	def Signal(self, pkt):
		global SIG
		if sw == '2':
			SIG = pkt[Dot11Common].Antsignal

		if sw == '1':
			SIG = -(256-ord(pkt.notdecoded[-2:-1]))



	def EAP_Identity(self, pkt):
		global sender
		global ap
		global user
		
		ap = str(pkt[Dot11].addr1)
		sender = str(pkt[Dot11].addr2)
		user = str(pkt[EAP].identity)	


	def ENC(self, pkt):
			global temp
			global ENC
			global CHR
			global ATH
			ENC = ""
			capability = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
                {Dot11ProbeResp:%Dot11ProbeResp.cap%}") 
			temp = pkt
			while temp:
				temp = temp.getlayer(Dot11Elt) 
				if temp and temp.ID == 48:
					ENC += "WPA2"	
					tr = temp.info
					temp= str(tr).encode("hex")
					t = RSN_ENC()
					t.Cipher_Suite()
					t.Auth_Management()
					return
				elif temp and temp.ID == 221 and str(temp.info).encode("hex").startswith("0050f2010100"):
					ENC += "WPA"
					tr = temp.info
					temp= str(tr).encode("hex")
					t = RSN_ENC()
					t.Cipher_Suite()
					t.Auth_Management()
					return
				temp = temp.payload
			if not ENC:
				if re.search("privacy", capability):
					ENC = "WEP"
					CHR = ""
					ATH = ""
				else:
					ENC = "OPEN"
					CHR = ""
					ATH = ""


			

class RSN_ENC:
	def __int__(self, temp):
		self.temp = temp

	def Cipher_Suite(self):
		global CHR
		GCS = temp
		if ENC =="WPA":

			if GCS[16:24] == "0050f204":
				CHR = 'CCMP/TKIP'
			elif GCS[16:24] == "f2020200": 
				CHR = 'TKIP'
			elif GCS[8:16] == '0050f204':
				CHR = 'CCMP'
		elif ENC == "WPA2":		
			if GCS[4:12] == "000fac02":
				if GCS[16:24] == "000fac04":
					CHR = "CCMP/TKIP"
				else:
					CHR = "TKIP"
			elif GCS[4:12] == "000fac04":
				CHR = "CCMP"
		else:
			CHR = ""

	def Auth_Management(self):
		global ATH
		Auth = temp
		if Auth[36:44] == "000fac01":
			ATH = "MGT"
		elif Auth[36:44] == "000fac02":
			ATH = "PSK"
		elif Auth[28:36] == "000fac01":
			ATH = "MGT"
		elif Auth[28:36] == "000fac02":
			ATH =  "PSK"
		elif Auth[32:40]== "0050f202":
			ATH = "PSK"
		else:
			ATH = " "

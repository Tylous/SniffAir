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



import sys
import time
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

###################################################
"""
Bugs/To do:
-CHR varible sometimes errors with:
"global name 'CHR' is not defined"
-clean up code
-create sql statements
"""
###################################################

class packet_sniffer():
	def __int__(self):
		super(Sniffer,self).__init__()

	def run(self):
	    sniff(iface="wlan0", count=0 ,prn=self.Sniffer)

	def Sniffer(self, pkt):
		if pkt.haslayer(Dot11Beacon):
			if pkt.type == 0 and pkt.subtype == 8 : ## unnesscary duplicate of above
				self.MAC(pkt)
				self.SSID(pkt)
				self.Channel(pkt)
				self.Signal(pkt)
				self.ENC(pkt)
				print "Beacon: %s, %s, %s, %s, %s, %s, %s " % (SSID, MAC, CHL, SIG, CHR, ENC, ATH) 
			
		elif pkt.haslayer(Dot11ProbeReq):
			self.MAC(pkt)
			self.SSID(pkt)
			self.Signal(pkt)
			print "Probe Req: %s, %s, %s " % (SSID, MAC, SIG)	

		elif pkt.haslayer(Dot11ProbeResp):
			self.MAC(pkt)
			self.SSID(pkt)
			self.Channel(pkt)
			self.Signal(pkt)
			self.ENC(pkt)
			self.Resp_Probe_Client_Mac(pkt)
			print "Probe Resp: %s, %s,  %s, %s, %s, %s, %s. Sending to: %s " % (SSID, MAC, CHL, SIG, ENC, CHR, ATH, RPCM) 
			
	def Resp_Probe_Client_Mac(self, pkt):
		global RPCM
		RPCM = pkt.addr1
	def SSID(self, pkt):
		global SSID
		SSID = str(pkt[Dot11Elt:1].info)

	def MAC(self, pkt):
		global MAC
		MAC = pkt.addr2

	def Channel(self, pkt):
		global CHL
		CHL = int(ord(pkt[Dot11Elt:3].info))

	def Signal(self, pkt):
		global SIG
		SIG = str(pkt.dBm_AntSignal)

	def ENC(self, pkt):

		global temp
		global ENC
		temp = pkt
		while temp:
			temp = temp.getlayer(Dot11Elt) 
			if temp and temp.ID == 48:
				ENC = "WPA2"	
				tr = temp.info
				temp= str(tr).encode("hex")
				t = RSN_ENC()
				t.Cipher_Suite()
				t.Auth_Management()
				return
			elif temp and temp.ID == 221 and str(temp.info).encode("hex").startswith("0050f20101000"):
				ENC = "WPA"
				tr = temp.info
				temp= str(tr).encode("hex")
				return
			temp = temp.payload

	def EAP_Identity(self, pkt):
		if pkt.haslayer(EAP):
					#if pkt[EAP].type ==1 :
						if len(pkt[EAP].identity) > 0:
					 		AUTHID=pkt[EAP].identity
							if AUTHID not in AUTHID_LIST:
								AUTHID_LIST.append(AUTHID)
								user=str(AUTHID_LIST)

class RSN_ENC:
	def __int__(self, temp):
		self.temp = temp

	def Cipher_Suite(self):
		global CHR
		GCS = temp[4:12]
		if GCS == "000fac01":
			CHR = "WEP"
		if GCS == "000fac02":
			CHR =  "TKIP"
		if GCS == "000fac04":
			CHR = "CCMP"
		if GCS == "000fac05":
			CHR = "WEP"			

	def Auth_Management(self):
		global ATH
		Auth = temp[28:36]
		if Auth == "000fac01":
			ATH = "MGT"
		if Auth == "000fac02":
			ATH =  "PSK"


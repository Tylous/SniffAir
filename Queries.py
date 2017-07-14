#!/usr/bin/python

from menu import *
import menu
from Connect2DB import *
import Connect2DB
import sqlite3
from sqlite3 import Error
import pandas as dp
from pandas import *
import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.CRITICAL)
from scapy.all import *



tables = ['accessPoints', 'ProbeRequests', 'ProbeResponses','EAP']
 
class queries():
	def __int__(self):
		super(queries, self).__init__()
	
	def blockPrint(self):
		sys.stdout = open(os.devnull, 'w')

	def enablePrint(self):
		sys.stdout = sys.__stdout__

	global inscope
	inscope = []
	tables = ['accessPoints', 'ProbeRequests', 'ProbeResponses','EAP']
	dp.set_option('display.width', None)
	dp.set_option('display.max_rows', None)



	def db_connect(self, workspace):
		global con
		con = sqlite3.connect(workspace)
		return con

	def clean_up(self):
		tb_value = 0
		for tb in tables:
			try:
				qr = dp.read_sql('select * from '+ tb +'', con)
				if tb_value == 0:
					test = qr.sort_values('sigStr', ascending=False).drop_duplicates(subset=['essid', 'bssid', 'vendor', 'channel', 'encryption', 'cipher', 'auth'], keep='first')					
				elif tb_value == 1:
					test = qr.sort_values('sigStr', ascending=False).drop_duplicates(subset=['essid', 'client', 'vendor'], keep='first')
				elif tb_value == 2:
					test = qr.sort_values('sigStr', ascending=False).drop_duplicates(subset=['essid', 'bssid', 'vendor', 'channe', 'encryption', 'cipher', 'auth', 'client'], keep='first')					
				elif tb_value == 3:
					test = qr.drop_duplicates(subset=['sender_mac', 'username', 'bssid'], keep='first')
				clrdb = test
				tb_value += 1
				clrdb.reset_index(inplace=True)
				clrdb.index.name="ID"
				clrdb.index = clrdb.index + 1
				del clrdb['index']
				clrdb.to_sql(""+tb+"", con , if_exists="replace")
			except pandas.io.sql.DatabaseError: 
				continue	


	def show_table(self, option):
		if option in ["AP"]:
			qr = dp.read_sql('select * from accessPoints', con)
			print qr.to_string(index=False)
		elif option in ["proberequests"]:
			qr = dp.read_sql('select * from ProbeRequests', con)
			print qr.to_string(index=False)
		elif option in ["proberesponses"]:
			qr = dp.read_sql('select * from ProbeResponses', con)
			print qr.to_string(index=False)
		elif option in ["EAP"]:
			qr = dp.read_sql('select * from EAP', con)
			print qr.to_string(index=False)
		else: 
			print "Error: Invalid query, please try again.\n"

	def in_scope(self, option):
		test = 'SSIDS'
		self.blockPrint()
		self.show(test)### modify with a return call
		self.enablePrint()
		if option in result:
			nwssid = dp.DataFrame({'essid' : [''+option+'']})
			inscpssid = dp.read_sql('select * from INSCOPE_SSIDS', con)
			inscpssid = inscpssid.append(nwssid)
			inscpssid = inscpssid.drop_duplicates()#subset=['essid'], keep='first')
			inscpssid.to_sql("INSCOPE_SSIDS",  con, index=False, if_exists="replace")
			for tb in tables:
				try:
					qr = dp.read_sql('select * from '+ tb + ' where essid = \"'+ option +'\"', con)
					del qr['ID']
					qr.reset_index(inplace=True)
					qr.index.name="ID"
					qr.index = qr.index + 1
					del qr['index']
					qr.to_sql("inscope_"+tb+"", con , if_exists="append")
					insqr = dp.read_sql('select * from inscope_'+tb+'', con)
					insqr = insqr.drop_duplicates()
					del insqr['ID']
					insqr.reset_index(inplace=True)
					insqr.index.name="ID"
					insqr.index = insqr.index + 1
					del insqr['index']
					insqr.to_sql("inscope_"+tb+"", con , if_exists="replace")
				except pandas.io.sql.DatabaseError: 
					continue	
		else:
			print "SSID does not exist"

	def main(self, t2, where):
		global result
		result = dp.DataFrame()
		for tb in tables:
			try:
				qr = dp.read_sql('' + t2 +' '+ tb + where +'', con)
				result = result.append(qr)
			except pandas.io.sql.DatabaseError: 
				continue
			
		result = result.drop_duplicates()
		result = result.to_string(index=False, header=False)
			
	def show(self, option):
		where = ''
		if option in ["SSIDS"]:
			t2 = "select essid from "
			self.main(t2, where)
			print str(result)
		elif option in ["AP_MAC"]:
			t2 = "select bssid from "
			self.main(t2, where)
			print str(result)
		elif option in ["Vendor"]:
			t2 = "select vendor from "
			self.main(t2, where)
			print str(result)
		elif option in ["Clients"]:
			t2 = "select client from "
			self.main(t2, where)
			print str(result)
		elif option in ["usernames"]:
			t2 = "select username from EAP "
			self.main(t2, where)
			print str(result)
		elif option in ["Channel"]:
			t2 = "select channel from "
			self.main(t2, where)
			print str(result)
		elif option in ["Encryption Type"]:
			t2 = "select encryption, auth, cipher from "
			self.main(t2, where)
			print str(result)

	def show_inscope_ssids(self):
		qr = dp.read_sql('select essid from INSCOPE_SSIDS', con)
		#result = qr.to_string(index=False, header=False)
		result = qr.to_string(formatters={'essid':'{{:<{}s}}'.format(qr['essid'].str.len().max()).format}, header=False, index=False)
		return str(result)
		

	def hidderDone(self, pkt):
		hidden_ssid_aps = set()
		if pkt.haslayer(Dot11Beacon):
			if len(pkt.info) <= 1:
				if pkt.addr3 not in hidden_ssid_aps:
					 hidden_ssid_aps.add(pkt.addr3)

		elif pkt.haslayer(Dot11ProbeResp) and (pkt.addr3 in hidden_ssid_aps):
			hiddenShit = dp.DataFrame({'essid' : [''+pkt.info+''], 'bssid' : [''+pkt.addr3+'']})
			hiddenShit.to_sql("Hidden_SSID", con , if_exists="append")
			f = dp.read_sql("select * from accesspoints", con)
			f.loc[f['bssid'] == pkt.addr3, 'essid'] = pkt.info
			del f['ID']
			f.reset_index(inplace=True)
			f.index.name="ID"
			f.index = fuckingthingy.index + 1
			del f['index']
			f.to_sql("accessPoints", con, if_exists="replace")


	def hidderDone_sniff(self, path):
		sniff(offline=path, count=0, store=0, prn = self.hidderDone)
		print "[+] Passive Hidden SSID Search Completed"
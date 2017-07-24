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
					table = qr.sort_values('PWR', ascending=False).drop_duplicates(subset=['ESSID', 'BSSID', 'VENDOR', 'CHAN', 'ENC', 'CIPHER', 'AUTH'], keep='first')                   
				elif tb_value == 1:
					table = qr.sort_values('PWR', ascending=False).drop_duplicates(subset=['ESSID', 'CLIENT', 'VENDOR'], keep='first')
				elif tb_value == 2:
					table = qr.sort_values('PWR', ascending=False).drop_duplicates(subset=['ESSID', 'BSSID', 'VENDOR', 'CHAN', 'ENC', 'CIPHER', 'AUTH', 'CLIENT'], keep='first')                 
				elif tb_value == 3:
					table = qr.drop_duplicates(subset=['SRC_MAC', 'USERNAME', 'BSSID'], keep='first')
				clrdb = table
				tb_value += 1
				clrdb.reset_index(inplace=True)
				clrdb.index.name="ID"
				clrdb.index = clrdb.index + 1
				del clrdb['index']
				clrdb.to_sql(""+tb+"", con , if_exists="replace")
			except pandas.io.sql.DatabaseError: 
				continue  

	def Custom_Queries(self, option):
		try:
			CQ = option
			if 'AP' in CQ:
				CQ = CQ.replace("AP","accessPoints")
			if 'proberequests' in CQ:
				CQ = CQ.replace("proberequests","ProbeRequests")
			if 'proberesponses' in CQ:
				CQ = CQ.replace("proberesponses","ProbeResponses")
			qr = dp.read_sql(CQ, con)
			print qr.to_string(index=False)
		except pandas.io.sql.DatabaseError:
			pass  


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
		elif option in ["hiddenssids"]:
			qr = dp.read_sql('select * from Hidden_SSID', con)
			print qr.to_string(index=False)
		elif option in ["EAP"]:
			qr = dp.read_sql('select * from EAP', con)
			print qr.to_string(index=False)
		else: 
			print "Error: Invalid query, please try again.\n"

	def in_scope(self, option):
		showvar = 'SSIDS'
		self.blockPrint()
		self.show(showvar)### modify with a return call
		self.enablePrint()
		if option in result:
			nwssid = dp.DataFrame({'ESSID' : [''+option+'']})
			inscpssid = dp.read_sql('select * from INSCOPE_SSIDS', con)
			inscpssid = inscpssid.append(nwssid)
			inscpssid = inscpssid.drop_duplicates()#subset=['essid'], keep='first')
			inscpssid.to_sql("INSCOPE_SSIDS",  con, index=False, if_exists="replace")
			for tb in tables:
				try:
					qr = dp.read_sql('select * from '+ tb + ' where ESSID = \"'+ option +'\"', con)
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
			t2 = "select ESSID from "
			self.main(t2, where)
			print str(result).replace(" ","")
		elif option in ["AP_MAC"]:
			t2 = "select BSSID from "
			self.main(t2, where)
			print str(result).replace(" ","")
		elif option in ["Vendor"]:
			t2 = "select VENDOR from "
			self.main(t2, where)
			print str(result).replace(" ","")
		elif option in ["Clients"]:
			t2 = "select CLIENT from "
			self.main(t2, where)
			print str(result).replace(" ","")
		elif option in ["Usernames"]:
			t2 = "select USERNAME from EAP "
			self.main(t2, where)
			print str(result).replace(" ","")
		elif option in ["Channel"]:
			t2 = "select CHAN from "
			self.main(t2, where)
			print str(result).replace(" ","")
		elif option in ["Encryption"]:
			t2 = "select ENC, AUTH, CIPHER from "
			self.main(t2, where)
			print str(result).replace(" ","")

	def show_inscope_ssids(self):
		qr = dp.read_sql('select ESSID from INSCOPE_SSIDS', con)
		result = qr.to_string(formatters={'ESSID':'{{:<{}s}}'.format(qr['ESSID'].str.len().max()).format}, header=False, index=False)
		return str(result)
		

	def hidderDone(self, pkt):
		hidden_ssid_aps = set()
		if pkt.haslayer(Dot11Beacon):
			if len(pkt.info) <= 1:
				if pkt.addr3 not in hidden_ssid_aps:
					 hidden_ssid_aps.add(pkt.addr3)

		elif pkt.haslayer(Dot11ProbeResp) and (pkt.addr3 in hidden_ssid_aps):
			hiddenStuff = dp.DataFrame({'ESSID' : [''+pkt.info+''], 'BSSID' : [''+pkt.addr3+'']})
			hiddenStuff.to_sql("Hidden_SSID", con , if_exists="append")
			f = dp.read_sql("select * from accesspoints", con)
			f.loc[f['BSSID'] == pkt.addr3, 'ESSID'] = pkt.info
			del f['ID']
			f.reset_index(inplace=True)
			f.index.name="ID"
			f.index = f.index + 1
			del f['index']
			f.to_sql("accessPoints", con, if_exists="replace")


	def hidderDone_sniff(self, path):
		sniff(offline=path, count=0, store=0, prn = self.hidderDone)
		print "[+] Passive Hidden SSID Search Completed\n"
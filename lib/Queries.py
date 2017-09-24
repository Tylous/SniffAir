#!/usr/bin/python

from Connect2DB import *
import Connect2DB
import sqlite3
from sqlite3 import Error
import pandas as dp
from pandas import *
import sys
from tabulate import tabulate

class colors:
    GRN = '\033[92m'
    RD = '\033[91m'
    NRM = '\033[0m'


tables = ['accessPoints', 'ProbeRequests', 'ProbeResponses','EAP']
try:
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
			try:
				global con
				con = sqlite3.connect(workspace)
				return con
			except ValueError:
				return

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
				print (tabulate(qr.drop_duplicates(), showindex=False, headers=qr.columns, tablefmt="psql"))
			except pandas.io.sql.DatabaseError:
				pass  


		def show_table(self, option):
			try:
				if option in ["AP"]:
					qr = dp.read_sql('select * from accessPoints', con)
					print (tabulate(qr.drop_duplicates(), showindex=False, headers=qr.columns, tablefmt="psql")) 
				elif option in ["proberequests"]:
					qr = dp.read_sql('select * from ProbeRequests', con)
					print (tabulate(qr.drop_duplicates(), showindex=False, headers=qr.columns, tablefmt="psql"))
				elif option in ["proberesponses"]:
					qr = dp.read_sql('select * from ProbeResponses', con)
					print (tabulate(qr.drop_duplicates(), showindex=False, headers=qr.columns, tablefmt="psql"))
				elif option in ["inscope_AP"]:
					qr = dp.read_sql('select * from inscope_accessPoints', con)
					print (tabulate(qr.drop_duplicates(), showindex=False, headers=qr.columns, tablefmt="psql")) 
				elif option in ["inscope_proberequests"]:
					qr = dp.read_sql('select * from inscope_proberequests', con)
					print (tabulate(qr.drop_duplicates(), showindex=False, headers=qr.columns, tablefmt="psql"))
				elif option in ["inscope_proberesponses"]:
					qr = dp.read_sql('select * from inscope_proberesponses', con)
					print (tabulate(qr.drop_duplicates(), showindex=False, headers=qr.columns, tablefmt="psql"))
				elif option in ["hiddenssids"]:
					qr = dp.read_sql('select * from Hidden_SSID', con)
					print (tabulate(qr.drop_duplicates(), showindex=False, headers=qr.columns, tablefmt="psql"))
				elif option in ["EAP"]:
					qr = dp.read_sql('select * from EAP', con)
					print (tabulate(qr.drop_duplicates(), showindex=False, headers=qr.columns, tablefmt="psql"))
				elif option in ["LOOT"]:
					qr = dp.read_sql('select * from LOOT', con)
					print (tabulate(qr.drop_duplicates(), showindex=False, headers=qr.columns, tablefmt="psql"))
				else: 
					print colors.RD + "Error: Invalid query, please try again.\n" + colors.NRM
			except pandas.io.sql.DatabaseError:
				print colors.RD + "Error: Table does not exist or is empty, please try again.\n" + colors.NRM

		def in_scope(self, option):
			showvar = 'SSIDS'
			self.blockPrint()
			self.show(showvar)
			self.enablePrint()
			if option in result:
				nwssid = dp.DataFrame({'ESSID' : [''+option+'']})
				inscpssid = dp.read_sql('select * from INSCOPE_SSIDS', con)
				inscpssid = inscpssid.append(nwssid)
				inscpssid = inscpssid.drop_duplicates()
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
			result = tabulate(result, showindex=False) 
				
		def show(self, option):
			where = ''
			if option in ["SSIDS"]:
				t2 = "select ESSID from "
				self.main(t2, where)
				print result.strip()
			elif option in ["AP_MAC"]:
				t2 = "select BSSID from "
				self.main(t2, where)
				print result.strip()
			elif option in ["Vendor"]:
				t2 = "select VENDOR from "
				self.main(t2, where)
				print result.strip()
			elif option in ["Clients"]:
				t2 = "select CLIENT from "
				self.main(t2, where)
				print result.strip()
			elif option in ["Usernames"]:
				t2 = "select USERNAME from EAP "
				self.main(t2, where)
				print result.strip()
			elif option in ["Channel"]:
				t2 = "select CHAN from "
				self.main(t2, where)
				print result.strip()
			elif option in ["Encryption"]:
				t2 = "select ENC, AUTH, CIPHER from "
				self.main(t2, where)
				print result.strip()

		def show_inscope_ssids(self):
			qr = dp.read_sql('select ESSID from INSCOPE_SSIDS', con)
			result = qr.to_string(formatters={'ESSID':'{{:<{}s}}'.format(qr['ESSID'].str.len().max()).format}, header=False, index=False)
			return str(result)

		def loot(self, loot):
			cl = dp.DataFrame(loot, index=[0])
			cl = cl[['MAC', 'Username', 'Password']]
			cl.reset_index(inplace=True)
			del cl['index']
			cl.to_sql("LOOT", con, index=False, if_exists="append")	
except NameError:
	pass
	print colors.RD + "Error: No workspace selected. Please Create or load a work" + colors.NRM

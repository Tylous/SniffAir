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

tables = ['EAP','accessPoints', 'ProbeRequests', 'ProbeResponses']
 
class queries():
	def __int__(self):
		super(queries, self).__init__()


	tables = ['EAP','accessPoints', 'ProbeRequests', 'ProbeResponses']
	dp.set_option('display.width', None)
	dp.set_option('display.max_rows', None)



	def db_connect(self, workspace):
		global con
		con = sqlite3.connect(workspace)

	def clean_up(self, workspace):
		con = self.db_connect()
		for tb in tables:
			qr = dp.read_sql('select * from '+ tb +'', con) 
			clrdb = qr.drop_duplicates()
			clrdb.reset_index(inplace=True)
			clrdb.index.name="ID"
			clrdb.index = clrdb.index + 1
			del clrdb['index']
			clrdb.to_sql(""+tb+"", t , if_exists="replace")


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

	def main(self, t2):
		results = []
		for tb in tables:
			try:
				#qr = dp.read_sql('select '+ t2 +' from '+ tb +'', con)
				qr = dp.read_sql('' + t2 +' '+ tb +'', con)
				clrdb = qr.drop_duplicates()
				tr = clrdb.values
				for r in tr:
					if r not in results:
						results.append(r)
						print str(r)[1:-1].replace('u','').replace('\'', '')
						continue	
		#except pandas.io.sql.DatabaseError:
			except pandas.io.sql.DatabaseError: 
				continue
			
	def show(self, option):
		if option in ["SSIDS"]:
			t2 = "select essid from "
			self.main(t2)
		elif option in ["AP_MAC"]:
			t2 = "select bssid from "
			self.main(t2)
		elif option in ["Vendor"]:
			t2 = "select vendor from "
			self.main(t2)
		elif option in ["Clients"]:
			t2 = "select client from "
			self.main(t2)
		elif option in ["usernames"]:
			t2 = "select username from EAP "
			self.main(t2)
		elif option in ["Channel"]:
			t2 = "select channel from "
			self.main(t2)
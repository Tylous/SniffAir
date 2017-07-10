#!/usr/bin/python

from menu import *
import menu
from Connect2DB import *
import Connect2DB
import sqlite3
from sqlite3 import Error
import pandas as dp
from pandas import *
import Query
import sys

 


tables = ['accessPoints', 'ProbeRequests', 'ProbeResponses']


dp.set_option('display.width', None)
dp.set_option('display.max_rows', None)



def clean_up(workspace):
	tables = ['accessPoints', 'ProbeRequests', 'ProbeResponses', 'EAP']
	t = sqlite3.connect(workspace)
	for tb in tables:
		qr = dp.read_sql('select * from '+ tb +'', t) 
		clrdb = qr.drop_duplicates()
		clrdb.reset_index(inplace=True)
		clrdb.index.name="ID"
		clrdb.index = clrdb.index + 1
		del clrdb['index']
		clrdb.to_sql(""+tb+"", t , if_exists="replace")


def show_table(workspace, option):
	t = sqlite3.connect(workspace)
	if option in ["AP"]:
		qr = dp.read_sql('select * from accessPoints', t)
		print qr.to_string(index=False)
	elif option in ["proberequests"]:
		qr = dp.read_sql('select * from ProbeRequests', t)
		print qr.to_string(index=False)
	elif option in ["proberesponses"]:
		qr = dp.read_sql('select * from ProbeResponses', t)
		print qr.to_string(index=False)
	elif option in ["EAP"]:
		qr = dp.read_sql('select * from EAP', t)
		print qr.to_string(index=False)
	else: 
		print "Error: Invalid query, please try again.\n"


def show(workspace, option):
	tables = ['accessPoints', 'ProbeRequests', 'ProbeResponses', 'EAP']
	#for tb in tables:
	t = sqlite3.connect(workspace)
	try:
		if option in ["SSIDS"]:
			list1 = []
			for tb in tables[0:3]:
				qr = dp.read_sql('select essid from '+ tb +'', t)
				clrdb = qr.drop_duplicates()
				tr = clrdb.values
				for r in tr:
					if r not in list1:
						list1.append(r)
						print str(r)[1:-1].replace('u','').replace('\'', '')

		elif option in ["AP_MAC"]:
			list1 = []
			for tb in tables:
				qr = dp.read_sql('select bssid from '+ tb +'', t)
				clrdb = qr.drop_duplicates()
				tr = clrdb.values
				for r in tr:
					if r not in list1:
						list1.append(r)
						print str(r)[1:-1].replace('u','').replace('\'', '')

		elif option in ["Vendor"]:
			list1 = []
			for tb in tables[0:3]:
				qr = dp.read_sql('select vendor from '+ tb +'', t)
				clrdb = qr.drop_duplicates()
				tr = clrdb.values
				for r in tr:
					if r not in list1:
						list1.append(r)
						print str(r)[1:-1].replace('u','').replace('\'', '')

		elif option in ["Clients"]:
			list1 = []
			for tb in tables[0:3]:
				qr = dp.read_sql('select client from '+ tb +'', t)
				clrdb = qr.drop_duplicates()
				tr = clrdb.values
				for r in tr:
					if r not in list1:
						list1.append(r)
						print str(r)[1:-1].replace('u','').replace('\'', '')

		elif option in ["username"]:
			list1 = []
			qr = dp.read_sql('select username from EAP', t)
			clrdb = qr.drop_duplicates()
			tr = clrdb.values
			for r in tr:
				if r not in list1:
					list1.append(r)
					print str(r)[1:-1].replace('u','').replace('\'', '')

	except pandas.io.sql.DatabaseError:
		return

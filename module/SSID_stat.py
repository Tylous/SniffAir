#!/usr/bin/python
import sqlite3
import pandas as dp
import pandas
import Queries
from Queries import *
from prettytable import PrettyTable


def main(workspace):
	tables = ['accessPoints', 'ProbeResponses','EAP']
	varibles = ['BSSID','VENDOR','CHAN', 'ENC, AUTH, CIPHER']
	info = ['','','','']
	title = ['BSSID','Vendors','Channels','Encrpytion']
	ws = workspace
	q = queries()
	ws1 = q.db_connect(ws)
	sql = dp.read_sql('select * from INSCOPE_SSIDS', ws1)
	if sql.empty:
		print "No inscope SSIDSs found, please add a SSID before running this module again.\n"
		return
	else:
		result = str(q.show_inscope_ssids())#.replace(" ",""))
		result = result.split('\n')
		for SSID in result:
			j = 0
			row = []
			for v in varibles:
				try:
					t2 = 'select '+ v +' from '
					where = ' where ESSID = \"'+ SSID +'\"'
					result = dp.DataFrame()
					for tb in tables:
						try:
							qr = dp.read_sql('' + t2 +' '+ tb + where +'', ws1)
							result = result.append(qr)
						except pandas.io.sql.DatabaseError: 
							continue
					result = result.drop_duplicates()
					result = result.to_string(index=False, header=False)

					info[j] = result
					row.append(info[j])
					j +=1
				except ValueError:
					continue	  
			print 'SSID:'+ SSID
			x = PrettyTable(title)
			x.add_row(row)
			print x

#main()

#!/usr/bin/python
import sys
#sys.path.insert(0, '../lib/')
import sqlite3
import pandas as dp
import Queries
from Queries import *


def main(workspace, path, name):
	table_name = ['accessPoints', 'ProbeRequests', 'ProbeRequests', 'EAP', 'Hidden_SSID', 'inscope_accessPoints', 'inscope_ProbeRequests', 'inscope_ProbeResponses']
	sheet_name = ['AccessPoints', 'ProbeRequests', 'ProbeRequests', 'EAP', 'Hidden_SSID', 'Inscope_AccessPoints', 'Inscope_ProbeRequests', 'Inscope_ProbeResponses']
	ws = workspace
	q = queries()
	ws1 = q.db_connect(ws)
	writer = dp.ExcelWriter(path+name+'.xlsx', engine='xlsxwriter')
	j = 0
	for tbn in table_name:
		try:
			td = dp.read_sql('select * from '+tbn+'', ws1)
			print tbn
			print sheet_name[j]
			if td.empty:
				pass
				j +=1
				print td
			else:
				print td
				td.to_excel(writer, sheet_name=''+sheet_name[j]+'', index=False)
				j +=1
		except ValueError:
			continue
		except pandas.io.sql.DatabaseError:
			continue
	print "Exporting: "+path+name+'.xlsx'
	writer.save()
	print "Completed"

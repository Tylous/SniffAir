#!/usr/bin/python
import sys
#sys.path.insert(0, '../lib/')
import sqlite3
import pandas as dp
import Queries
from Queries import *

class colors:
    GRN = '\033[92m'
    RD = '\033[91m'
    NRM = '\033[0m'


def main(workspace, path, name):
	table_name = ['accessPoints', 'ProbeRequests', 'ProbeRequests', 'EAP', 'Hidden_SSID', 'inscope_accessPoints', 'inscope_ProbeRequests', 'inscope_ProbeResponses']
	sheet_name = ['AccessPoints', 'ProbeRequests', 'ProbeRequests', 'EAP', 'Hidden_SSID', 'Inscope_AccessPoints', 'Inscope_ProbeRequests', 'Inscope_ProbeResponses']
	ws = workspace
	q = queries()
	ws1 = q.db_connect(ws)
	writer = dp.ExcelWriter(path+name+'.xlsx', engine='xlsxwriter')
	j = 0
	print "Exporting: "+path+name+'.xlsx'
	for tbn in table_name:
		try:
			td = dp.read_sql('select * from '+tbn+'', ws1)
			if td.empty:
				pass
				j +=1
				print colors.RD + "[-]" + colors.NRM + " Skipping: " + sheet_name[j] + ". No Data in table."
			else:
				td.to_excel(writer, sheet_name=''+sheet_name[j]+'', index=False)
				j +=1
				print colors.GRN + "[+]" + colors.NRM + " Exporting: " + sheet_name[j] + "."
		except ValueError:
			continue
		except pandas.io.sql.DatabaseError:
			continue
	writer.save()
	print "Export Completed"

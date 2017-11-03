#!/usr/bin/python
import sqlite3
import pandas as dp
import pandas
import Queries
from Queries import *

class colors:
    RD = '\033[91m'
    NRM = '\033[0m'

def main(workspace):
	ws = workspace
	q = queries()
	ws1 = q.db_connect(ws)
	query=dp.read_sql('select * from accessPoints', ws1)
	inscope=dp.read_sql('select * from INSCOPE_SSIDS', ws1)
	result = inscope.to_string(formatters={'ESSID':'{{:<{}s}}'.format(inscope['ESSID'].str.len().max()).format}, header=False, index=False)
	ENC = "OPEN"
	PWR = "-100"
	notssids = result.replace('\n','\' and ESSID not like \'')
	count = 1
	print "AP Hunter - Displays Access Points within a specific range, using a specific encrpytion type. These may be benign."
	print "-------------------------------------------------------------------------------------------------------------------------------------------"
	while count <=2:
		try:
			print "ENC currently set to: " + ENC + " and PWR currently set to: " + PWR +". Press Enter to see these results or to set the values either type ENC or PWR and then the value. Note that when setting the PWR you must include a \'-\'"
			input = raw_input(" >>")
			varible = input.split(' ')		
			if varible[0] == 'ENC':
				ENC = varible[1]
			if varible[0] == 'PWR':
				PWR = varible[1]
			if ENC and PWR:
				AP_HT = dp.read_sql("select * from accessPoints where ESSID not like '"+ notssids +"' and  ENC = '"+ENC+"' and  PWR >='"+PWR+"'", ws1)
				if AP_HT.empty:
					print colors.RD + "Query returned no  valid results, please try again.\n" + colors.NRM
				else:
					print (tabulate (AP_HT, showindex=False, headers=query.columns, tablefmt="psql"))
				print "To exit press Ctl+C"
		except KeyboardInterrupt:
			count = 3
			print "\033[1A"
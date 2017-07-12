#!/usr/bin/python
import sqlite3
import pandas as dp
import pandas
import Queries
from Queries import *
from prettytable import PrettyTable




def main():
	q = queries()
	q.db_connect(workspace)
	q.show('SSIDS')
	rawr = []
	rawr.append(Queries.result)
	print str(rawr)
	varibles = ['bssid','vendor','channel', 'encryption, auth, cipher']
	SSID = 'Odin'
	j = 0
	for v in varibles:
		t2 = 'select '+ v +' from '
		where = ' where essid = \"'+ SSID +'\"'

		q.main(t2, where)
		varibles[j] = Queries.result

		j +=1

	title = []
	row = []

	title.append("BSSID")
	row.append(varibles[0])
	title.append("Vendors")
	row.append(varibles[1])
	title.append("Channels")
	row.append(varibles[2])
	title.append("Encrpytion")
	row.append(varibles[3])
  
	print 'SSID:'+ SSID
	x = PrettyTable(title)
	x.add_row(row)
	print x

	#tables = ['accessPoints', 'ProbeRequests', 'ProbeResponses', 'EAP']

	#con = sqlite3.connect('ant')
	#result = dp.DataFrame()
	#for tb in tables:
	#	try:
			#qr = dp.read_sql('' + t2 +' '+ tb +'', con)


main()


#result = dp.DataFrame()
#		for tb in tables:
#			try:
#				qr = dp.read_sql('' + t2 +' '+ tb +'', con)
#				result = result.append(qr)
#			except pandas.io.sql.DatabaseError: 
#				continue
#			
#		result = result.drop_duplicates()
#		result = result.to_string(index=False, header=False)
#		result = result.replace(,'')
#		print str(result)
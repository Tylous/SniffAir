#!/usr/bin/python
import sqlite3
import pandas as dp
import pandas
import Queries
from Queries import *

def main(workspace):
	varibles = ['CHAN', 'VENDOR', 'ENC']
	msg = ['Channel', 'Vendor', 'Encryption']
	title = ['Channel - SniffAir noticed that the following APs are sitting on channels that are outside the norm from the rest of the APs in the network.', 'Vendor - SniffAir has discovered the following APs broadcasting an inscope ESSID but is from a different vendor then the rest of the network.', 'Encryption - Whoa! SniffAir discovered an AP running with a different type of encryption then the rest of the APs in that network!']
	ws = workspace
	q = queries()
	ws1 = q.db_connect(ws)
	inscope=dp.read_sql('select * from INSCOPE_SSIDS', ws1)
	result = inscope.to_string(formatters={'ESSID':'{{:<{}s}}'.format(inscope['ESSID'].str.len().max()).format}, header=False, index=False)
	ssidresult = str(q.show_inscope_ssids())
	ssidresult = ssidresult.split('\n')
	j = 0
	for v in varibles:
		try:
			result1 = dp.DataFrame()
			for SSID in ssidresult:
				query = dp.read_sql("select * from accessPoints where ESSID = '"+ SSID +"'", ws1)
				RA = query[v].value_counts()
				RA_result = RA.reset_index(name="count").query("count <2")["index"].tolist()
				for r in RA_result:
					y = query.loc[query[v].isin([str(r)])]
					result1 = y.append(result1)
			if result1.empty:
					print "[*] Nothing Suspicious regarding the " + msg[j] + "information"
					pass
			else:
				print title[j]
				print (tabulate(result1,showindex=False, headers=query.columns, tablefmt="psql"))+"\n"
			j +=1
		except ValueError:
			continue

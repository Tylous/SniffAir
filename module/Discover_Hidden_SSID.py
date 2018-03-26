import sys
import sqlite3
import pandas as dp
import pandas
sys.path.insert(0, '../lib/')
import Queries
from Queries import *

def main(workspace):
	ws = workspace
	q = queries()
	ws1 = q.db_connect(ws)
	try:
		AP = dp.read_sql('select BSSID from accessPoints where ESSID = "Hidden"', ws1)
		AP_BSSID = AP.to_string(index=False, header=False)
		AP_BSSID = AP_BSSID.split('\n')
		for v in AP_BSSID:
			PR_ESSID = dp.read_sql('select ESSID from ProbeResponses where BSSID="'+v+'"', ws1).drop_duplicates()
			PR_BSSID = dp.read_sql('select BSSID from ProbeResponses where BSSID="'+v+'"', ws1).drop_duplicates()
			HST = dp.concat([PR_ESSID, PR_BSSID], axis=1, join='inner')
			del HST['index']
			HST.to_sql("Hidden_SSID", ws1 , if_exists="append")
			rawr = dp.read_sql('select * from accessPoints', ws1)
			if PR_ESSID.empty:
				continue
			else:
				ESSID = PR_ESSID.to_string(index=False, header=False)
				ESSID = ESSID.split('\n')
				rawr.loc[rawr['BSSID'] == v, 'ESSID'] = ESSID
				del rawr['ID']
				rawr.reset_index(inplace=True)
				rawr.index.name="ID"
				rawr.index = rawr.index + 1
				del rawr['index']
				rawr.to_sql("accessPoints", ws1 , if_exists="replace")
				value_pr = PR_ESSID.to_string(index=False, header=False)
				print "DISCOVERED HIDDEN SSID. "+v+ " is actually: " +str(value_pr)

		HS = dp.read_sql('select * from Hidden_SSID', ws1)
		if HS.empty:
			print "NO SSIDS DISCOVERED"
		else:
			del HS['index']
			HS.reset_index(inplace=True)
			HS.index.name="ID"
			HS.index = HS.index + 1
			del HS['index']
			HS.to_sql("Hidden_SSID", ws1 , if_exists="replace")
			print "Completed"
	except KeyError:
		print "NO NEW SSIDS DISCOVERED."
		HS = dp.read_sql('select * from Hidden_SSID', ws1)
		print tabulate(HS, showindex=False, headers=HS.columns, tablefmt="psql")

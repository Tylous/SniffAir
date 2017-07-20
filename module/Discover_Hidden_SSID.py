import sqlite3
import pandas as dp
import pandas
import Queries
from Queries import *
import sys

def main(workspace):
	ws = workspace
	q = queries()
	ws1 = q.db_connect(ws)
	AP = dp.read_sql('select BSSID from accessPoints where ESSID = "Hidden"', ws1)
	AP_BSSID = AP.to_string(index=False, header=False)
	AP_BSSID = AP_BSSID.split('\n')
	for v in AP_BSSID:
		PR_ESSID = dp.read_sql('select ESSID from ProbeResponses where BSSID="'+v+'"', ws1).drop_duplicates()
		PR_ESSID.to_sql("Hidden_SSID", ws1 , if_exists="append")
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
	print "Completed"

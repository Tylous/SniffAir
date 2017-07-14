import sqlite3
import pandas as dp
import pandas
import Queries
import logging
logging.getLogger("scapy.runtime").setLevel(logging.CRITICAL)
from scapy.all import  *
from Queries import *
import sys

def main(workspace):
	ws = workspace
	q = queries()
	ws1 = q.db_connect(ws)
	AP = dp.read_sql('select bssid from accessPoints where essid = "Hidden"', ws1)
	AP_BSSID = AP.to_string(index=False, header=False)
	AP_BSSID = AP_BSSID.split('\n')
	for v in AP_BSSID:
		PR_ESSID = dp.read_sql('select essid from ProbeResponses where bssid="'+v+'"', ws1).drop_duplicates()
		PR_ESSID.to_sql("Hidden_SSID", ws1 , if_exists="append")
		rawr = dp.read_sql('select * from accessPoints', ws1)
		if PR_ESSID.empty:
			continue
		else:
			essid = PR_ESSID.to_string(index=False, header=False)
			essid = essid.split('\n')
			rawr.loc[rawr['bssid'] == v, 'essid'] = essid
			del rawr['ID']
			rawr.reset_index(inplace=True)
			rawr.index.name="ID"
			rawr.index = rawr.index + 1
			del rawr['index']
			rawr.to_sql("accessPoints", ws1 , if_exists="replace")
			value_pr = PR_ESSID.to_string(index=False, header=False)
			print "DISCOVERED HIDDEN SSID. "+v+ " is actually: " +str(value_pr)



import sqlite3
import sys
import pandas

connection = sqlite3.connect("good")
print pandas.read_sql_query('select essid, mac, channe  from ProbeResponses', connection)

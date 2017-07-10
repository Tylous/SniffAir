#!/usr/bin/python

from main import *
from Connect2DB import *
import Connect2DB
import sqlite3
from sqlite3 import Error
import pandas as dp

tables = ['accessPoints', 'ProbeRequests', 'ProbeResponses']


dp.set_option('display.width', None)
dp.set_option('display.max_rows', None)



def clean_up():
	connection = sqlite3.connect('ant1')

	for tb in tables:
		qr = dp.read_sql('select * from '+ tb +'', connection)
		clrdb = qr.drop_duplicates()
		clrdb.to_sql(""+tb+"", connection, if_exists="replace")



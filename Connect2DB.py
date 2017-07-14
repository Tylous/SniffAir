#!/usr/bin/python

import sys
import os
import sqlite3
from sqlite3 import Error
from Connect2DB import *



def db_name(name):
    global db_file
    #db_file = str(raw_input("Enter name of db: "))
    db_file = name

def create_connection():
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
	conn.execute('''CREATE TABLE accessPoints
            (essid, bssid, vendor, channel, sigStr, encryption, cipher, auth)''')
        conn.execute('''CREATE TABLE ProbeRequests
            (essid, client, vendor, sigStr)''')
        conn.execute('''CREATE TABLE ProbeResponses
            (essid, bssid, vendor, channe, sigStr, encryption, cipher, auth, client)''')
        conn.execute('''CREATE TABLE EAP
            (sender_mac, username, bssid)''')
        conn.execute('''CREATE TABLE INSCOPE_SSIDS
            (essid)''')
    except Error as e:
        conn.close()
    finally:
        conn.close()


def connect_db():
    global connection
    connection = sqlite3.connect(db_file)

class load():

    def insert_ACCESS_POINT(self, SSID, MAC, Vendor, CHL, SIG, ENC, CHR, ATH):
        connection.execute("insert into accessPoints (essid, bssid, vendor, channel, sigStr, encryption, cipher, auth) values (?,?,?,?,?,?,?,?)", (SSID, MAC, Vendor, CHL, SIG, ENC, CHR, ATH))
        connection.commit()
        connection.close() 

    def Insert_Probe_REQUEST(self, SSID, MAC, Vendor, SIG):
        connection.execute("insert into ProbeRequests (essid, client, vendor, sigStr) values (?,?,?,?)", (SSID, MAC, Vendor, SIG)) 
        connection.commit()
        connection.close() 

    def Insert_Probe_RESPONSE(self, SSID, MAC, Vendor, CHL, SIG, ENC, CHR, ATH, RPCM):
        connection.execute("insert into ProbeResponses (essid, bssid, vendor, channe, sigStr, encryption, cipher, auth, client) values (?,?,?,?,?,?,?,?,?)", (SSID, MAC, Vendor, CHL, SIG, ENC, CHR, ATH, RPCM))   
        connection.commit()
        connection.close() 

    def Insert_EAP(self, sender, user, ap):
        connection.execute("insert into EAP (sender_mac, username, bssid) values (?,?,?)", (sender, user, ap))   
        connection.commit()
        connection.close() 

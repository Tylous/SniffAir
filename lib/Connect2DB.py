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
            (ESSID, BSSID, VENDOR, CHAN, PWR, ENC, CIPHER, AUTH)''')
        conn.execute('''CREATE TABLE ProbeRequests
            (ESSID, CLIENT, VENDOR, PWR)''')
        conn.execute('''CREATE TABLE ProbeResponses
            (ESSID, BSSID, VENDOR, CHAN, PWR, ENC, CIPHER, AUTH, CLIENT)''')
        conn.execute('''CREATE TABLE EAP
            (SRC_MAC, USERNAME, BSSID)''')
        conn.execute('''CREATE TABLE INSCOPE_SSIDS
            (ESSID)''')
    except Error as e:
        conn.close()
    finally:
        conn.close()

def connect_db():
    global connection
    connection = sqlite3.connect(db_file, check_same_thread=False)
    connection.text_factory = str

class load():

    def insert_ACCESS_POINT(self, SSID, MAC, VENDOR, CHL, SIG, ENC, CHR, ATH):
        connection.execute("insert into accessPoints (ESSID, BSSID, VENDOR, CHAN, PWR, ENC, CIPHER, AUTH) values (?,?,?,?,?,?,?,?)", (SSID, MAC, VENDOR, CHL, SIG, ENC, CHR, ATH))
        connection.commit()
        connection.close() 

    def Insert_Probe_REQUEST(self, SSID, MAC, VENDOR, SIG):
        connection.execute("insert into ProbeRequests (ESSID, CLIENT, VENDOR, PWR) values (?,?,?,?)", (SSID, MAC, VENDOR, SIG)) 
        connection.commit()
        connection.close() 

    def Insert_Probe_RESPONSE(self, SSID, MAC, VENDOR, CHL, SIG, ENC, CHR, ATH, RPCM):
        connection.execute("insert into ProbeResponses (ESSID, BSSID, VENDOR, CHAN, PWR, ENC, CIPHER, AUTH, CLIENT) values (?,?,?,?,?,?,?,?,?)", (SSID, MAC, VENDOR, CHL, SIG, ENC, CHR, ATH, RPCM))   
        connection.commit()
        connection.close() 

    def Insert_EAP(self, sender, user, ap):
        connection.execute("insert into EAP (SRC_MAC, USERNAME, BSSID) values (?,?,?)", (sender, user, ap))   
        connection.commit()
        connection.close() 
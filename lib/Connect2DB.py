#!/usr/bin/python

import sys
import os
import subprocess
import sqlite3
from sqlite3 import Error
from Connect2DB import *
from tabulate import tabulate
import pandas as dp


def db_name(workspace):
    global db_file
    db_file = workspace

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
        conn.execute('''CREATE TABLE LOOT
            (MAC, USERNAME, PASSWORD)''')
    except Error as e:
        conn.close()
    finally:
        conn.close()


def list():
    db_list = str(os.listdir('db/'))[1:-1].replace('.db','').replace(',','').replace('\'','').split()
    dbl=[]
    for p in db_list:
        dbl.append("workspace load "+p)

def display_list():
    dl = str(os.listdir('db/'))[1:-1].replace(',','').replace('\'','')
    frame = dp.DataFrame(dl.split())
    print tabulate(frame, showindex=False, headers=['Workspaces'], tablefmt='psql')


def delete_workspace(workspace):
    subprocess.call('rm -rf db/'+workspace, shell=True)

def connect_db():
    global connection
    connection = sqlite3.connect(db_file, check_same_thread=False)
    connection.text_factory = str

class load():
        def __init__(self):
            pass

        def begin(self):
            connection.execute("BEGIN TRANSACTION")

        def insert_ACCESS_POINT(self, SSID, MAC, VENDOR, CHL, SIG, ENC, CHR, ATH):
            connection.execute("insert into accessPoints (ESSID, BSSID, VENDOR, CHAN, PWR, ENC, CIPHER, AUTH) values (?,?,?,?,?,?,?,?)", (SSID, MAC, VENDOR, CHL, SIG, ENC, CHR, ATH))

        def Insert_Probe_REQUEST(self, SSID, MAC, VENDOR, SIG):
            connection.execute("insert into ProbeRequests (ESSID, CLIENT, VENDOR, PWR) values (?,?,?,?)", (SSID, MAC, VENDOR, SIG))

        def Insert_Probe_RESPONSE(self, SSID, MAC, VENDOR, CHL, SIG, ENC, CHR, ATH, RPCM):
            connection.execute("insert into ProbeResponses (ESSID, BSSID, VENDOR, CHAN, PWR, ENC, CIPHER, AUTH, CLIENT) values (?,?,?,?,?,?,?,?,?)", (SSID, MAC, VENDOR, CHL, SIG, ENC, CHR, ATH, RPCM))


        def Insert_EAP(self, sender, user, ap):
            connection.execute("insert into EAP (SRC_MAC, USERNAME, BSSID) values (?,?,?)", (sender, user, ap))

        def Close(self):
            connection.commit()
            connection.close()
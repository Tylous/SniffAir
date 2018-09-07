#!/usr/bin/python

import logging
logging.getLogger ( "scapy.runtime" ).setLevel ( logging.CRITICAL )
from scapy.all import *
load_contrib ( 'ppi_cace' )
import sys, os, argparse
sys.path.insert ( 0, '../lib/' )
from Queries import *

parser = argparse.ArgumentParser ()
parser.add_argument ( '-S', '--ssid', metavar='SSID', dest='ssid', action='store', help=argparse.SUPPRESS, required=False )
parser.add_argument ( '-P', '--path', metavar='path', dest='path', action='store', help='path\n', required=False )
parser.add_argument ( '-W', '--workspace', metavar='database', dest='database', action='store', help='workspace name\n',required=True )

args = parser.parse_args ()

workspace = args.database
q = queries ()
ws = q.db_connect ( '../' + workspace )

class colors:
    RD = '\033[91m'
    NRM = '\033[0m'


Beacon = 0
ProbeRequest = 0
ProbeResponses = 0
EAPP = 0

def packet(pkt):
    global Beacon
    global ProbeRequest
    global ProbeResponses
    global EAPP
    try:
        if args.ssid:
            SSID_List = args.ssid
            MAC_List = str ( q.show_MACs ( SSID_List ) )
            MAC_List = MAC_List.split ( '\n' )
        else:
            sql = dp.read_sql ( 'select * from INSCOPE_SSIDS', ws )
            if sql.empty:
                print "No inscope SSIDSs found, please add a SSID before running this module again.\n"
                return
            else:
                SSID_List = str ( q.show_inscope_ssids () )
                SSID_List = SSID_List.split ( '\n' )
                MAC_List = str ( q.show_inscope_MACs () )
                MAC_List = MAC_List.split ( '\n' )

        if pkt.haslayer ( Dot11 ):
            if pkt.type == 0 and pkt.subtype == 8:
                SSID = pkt[Dot11Elt:1].info
                SSID = SSID.decode ( 'utf-8', 'ignore' )
                if SSID in SSID_List:
                    Beacon += 1
                    if args.path:
                        wrpcap (args.path + '/filtered.pcap', pkt, append=True )
                    else:
                        wrpcap ( path+'/filtered.pcap', pkt, append=True )
            elif pkt.type == 0 and pkt.subtype == 4:
                SSID = pkt[Dot11Elt:1].info
                SSID = SSID.decode ( 'utf-8', 'ignore' )
                if SSID in SSID_List:
                    ProbeRequest += 1
                    if args.path:
                        wrpcap (args.path + '/filtered.pcap', pkt, append=True )
                    else:
                        wrpcap (path+'/filtered.pcap', pkt, append=True )
            elif pkt.type == 0 and pkt.subtype == 5:
                MAC = pkt.addr2
                if MAC in MAC_List:
                    ProbeResponses += 1
                    if args.path:
                        wrpcap (args.path + '/filtered.pcap', pkt, append=True )
                    else:
                        wrpcap ( path+'/filtered.pcap', pkt, append=True )
        if pkt.haslayer ( EAP ):
            src_MAC = pkt[Dot11].addr2
            dst_MAC = pkt[Dot11].addr1
            if src_MAC in MAC_List or dst_MAC in MAC_List:
                EAPP += 1
                if args.path:
                    wrpcap (args.path + '/filtered.pcap', pkt, append=True )
                else:
                    wrpcap ( path+'/filtered.pcap', pkt, append=True )
    except pandas.io.sql.DatabaseError:
        print colors.RD + "Error: SSID does not exist.\n" + colors.NRM
        sys.exit()


path = workspace.split("/")
path = '/'.join(path[0:2])
path = "../" + path
for file in os.listdir(path):
    if file.endswith(".pcapdump"):
        fullpath = (os.path.join(path, file))
        print "[*] Parsing file : " + file
        sniff (offline=fullpath, count=0, store=0, prn=packet)

print "[*] "+ str(Beacon) + " Beacon Frames Added"
print "[*] "+ str(ProbeRequest) + " Probe Request Frames Added"
print "[*] "+ str(ProbeResponses) + " Probe Responses Frames Added"
print "[*] "+ str(EAPP) + " EAP Frames Added"

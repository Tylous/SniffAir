#!/usr/bin/python
import logging

logging.getLogger ( "scapy.runtime" ).setLevel ( logging.CRITICAL )
from scapy.all import *

load_contrib ( 'ppi_cace' )
import sys, os, time, signal, subprocess
import argparse

sys.path.insert ( 0, '../../lib/' )
from Queries import *

parser = argparse.ArgumentParser ()
parser.add_argument ( '-f', '--format', metavar='format', dest='format', action='store', help='Format JTR or Hashcat\n',required=True )
parser.add_argument ( '-s', '--ssid', metavar='SSID', dest='ssid', action='store', help=argparse.SUPPRESS, required=False )
parser.add_argument ( '-p', '--path', metavar='path', dest='path', action='store', help='path\n', required=False )
parser.add_argument ( '-w', '--workspace', metavar='database', dest='database', action='store', help='workspace name\n', required=True )
parser.add_argument ( '-i', '--inputfile', metavar='inputfile', dest='inputfile', action='store', help='input file path\n', required=False )

args = parser.parse_args ()

workspace = args.database
q = queries ()
ws = q.db_connect ( '../../' + workspace )


def test(pkts):
	global outpath
	if args.path:
		outpath = args.path
	else:
		outpath = path

	if args.ssid:
		SSID_List = args.ssid
		MAC_List = str ( q.show_MACs (SSID_List) )
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
			MAC_List = MAC_List.split( '\n' )

	for pkt in pkts:
		if Dot11Beacon in pkt:
			if str ( pkt[Dot11Elt:1].info ) == "":
				SSID = "Hidden"
			elif str ( pkt[Dot11Elt:1].info ).startswith ( "\000" ):
				SSID = "Hidden"
			else:
				SSID = pkt[Dot11Elt:1].info
				SSID = SSID.decode ( 'utf-8', 'ignore' )
			if SSID in SSID_List:
				wrpcap (outpath +'/filtered.pcap', pkt, append=True )

		if pkt.haslayer ( EAPOL ):
			EAPOLP = pkt[EAPOL]
			if EAPOLP.type == 3:
				if pkt.addr2 in MAC_List:
					if str ( EAPOLP )[6:8].encode ( "hex" ) == "8a00":
						wrpcap ( outpath + '/filtered.pcap', pkt, append=True )
						ascii_ap_mac = pkt.addr2
						ascii_client_mac = pkt.addr1
						aNonce = str ( EAPOLP )[17:49].encode ( "hex" )
						print "Frame 1"
						print "AP MAC: " + ascii_ap_mac
						print "Client MAC: " + ascii_client_mac
						print "ANonce: " + aNonce

				elif str ( EAPOLP )[6:8].encode ( "hex" ) == "0a00" and str ( EAPOLP )[99:123].encode ( "hex" ):
					if pkt.addr2 in MAC_List:
						wrpcap ( outpath + '/filtered.pcap', pkt, append=True )
						ascii_ap_mac = pkt.addr2
						ascii_client_mac = pkt.addr1
						sNonce = str ( EAPOLP )[17:49].encode ( "hex" )
						mic = str ( EAPOLP )[81:97].encode ( "hex" )
						data = str ( EAPOLP )[99:123].encode ( "hex" )
						print "Frame 2"
						print "AP MAC: " + ascii_ap_mac
						print "Client MAC: " + ascii_client_mac
						print "SNonce: " + sNonce
						print "MIC: " + mic
						print "Data: " + data
				else:
					return
if args.inputfile == "None":
	pullpath = args.inputfile
	sniff(offline=fullpath, count=0, store=0, prn=test)
else:
		path = workspace.split("/")
		path = '/'.join(path[0:2])
		path = "../../"+path
		for file in os.listdir (path):
			if file.endswith ( ".pcapdump" ):
				fullpath = (os.path.join ( path, file ))
				print fullpath
				sniff ( offline=fullpath, count=0, store=0, prn=test )


if args.format == "JTR":
	subprocess.call ( 'aircrack-ng -J' + outpath + '/filtered.pcap > ' +outpath + '/test1.hccap', shell=True )
	subprocess.call ( 'hccap2john '+ outpath +'/test1.hccap > '+ outpath +'/hccap.john', shell=True )
	print "john -wordlist=<path to wordlist> -format=wpapsk \"hccap.john\""

if args.format == "Hashcat":
	subprocess.call ( './cap2hccapx.bin filtered.pcap output.hccapx >/dev/null 2>&1', shell=True )
	print "oclHashcat64.exe -m 2500 -a3 capture.hccapx ?d?d?d?d?d?d?d?d"
	print "			or"
	print "oclHashcat64.exe -m 2500 -a0 <path to wordlist>  capture.hccapx"

if args.format == "both":
	subprocess.call ( './cap2hccapx.bin '+ outpath +'/filtered.pcap '+ outpath +'/output.hccapx >/dev/null 2>&1', shell=True )
	subprocess.call ( 'aircrack-ng -J '+ outpath +'/filtered.pcap '+ outpath +'/test1.hccap', shell=True )
	subprocess.call ( 'hccap2john '+ outpath +'/test1.hccap > '+ outpath +'/hccap.john', shell=True )
	print "john -wordlist=<path to wordlist> -format=wpapsk \"hccap.john\""
	print "oclHashcat64.exe -m 2500 -a3 capture.hccapx ?d?d?d?d?d?d?d?d"
	print "								or"
	print "oclHashcat64.exe -m 2500 -a0 <path to wordlist>  capture.hccapx"

subprocess.call ( 'rm -rf '+ outpath +'/filtered.pcap', shell=True )
subprocess.call ( 'rm -rf '+ outpath +'/test1.hccap', shell=True )

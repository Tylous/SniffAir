#!/usr/bin/python

import sys
import signal
import argparse
import logging
logging.getLogger ( "scapy.runtime" ).setLevel ( logging.CRITICAL )
from scapy.all import *

# Setup signal handler to catch CTRL-C
def signal_handler(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Get arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interface', metavar='interface', help='wireless interface to use', required=True)
parser.add_argument('-d', '--delay', metavar='delay', help='seconds to delay (default=.3)', default=.3, type=float)
parser.add_argument('-c', '--count', metavar='count', \
        help='number of packets to send per SSID per iteration (default=10)', default=10, type=int)
parser.add_argument('-m', '--mac', metavar='mac', help='last 3 octets of source mac address (default=00:11:22)', default='00:11:22')
ssid_group = parser.add_mutually_exclusive_group(required=True)
ssid_group.add_argument('-s', '--ssid', metavar='ssid', help='ssid name')
ssid_group.add_argument('-f', '--file', metavar='file', help='ssid file')
args = parser.parse_args()

# Create ssid list
ssids = []
if args.file == None:
    ssids.extend([args.ssid])
else:
    with open(args.file) as f:
        content = f.readlines()
        ssids = [x.strip() for x in content]

# Setup probe request packet
param = Dot11ProbeReq()
ratestr = '03\x12\x96\x18\x24\x30\x48\x60'
rates = Dot11Elt(ID='Rates',info=ratestr)
dst = 'ff:ff:ff:ff:ff:ff'

# Loop until CTRL-C
while True:
    for ssid in ssids:
        essid = Dot11Elt(ID='SSID',info=ssid)
        #dsset = Dot11Elt(ID='DSset',info='\x01')
        pkt = RadioTap()\
            /Dot11(type=0,subtype=4,addr1=dst,addr2=RandMAC()[0:9]+args.mac,addr3=dst)\
            /param/essid/rates

        print '[*] 802.11 Probe Request: SSID=[%s], count=%d' % (ssid,args.count)
        try:
            sendp(pkt,count=args.count,inter=args.delay,verbose=0,iface=args.interface)
        except:
            raise
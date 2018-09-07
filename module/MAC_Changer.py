#!/usr/bin/python

import sys, os, subprocess, argparse, time
parser = argparse.ArgumentParser ()
parser.add_argument ( '-I', '--Interface', metavar='iface', dest='iface', action='store', help= argparse.SUPPRESS, required=True )
parser.add_argument ( '-M', '--MAC', metavar='MAC', dest='MAC', action='store', help=argparse.SUPPRESS, required=False )
args = parser.parse_args ()

def MAC_Changer():
    subprocess.call ( 'ifconfig ' + args.iface +' down', shell=True )
    subprocess.call ( 'sudo macchanger --mac ' + args.MAC +' '+ args.iface, shell=True )
    subprocess.call ( 'ifconfig ' + args.iface + ' up', shell=True )
    #print "Interface " + args.iface + " new MAC Address:" + args.MAC

MAC_Changer()
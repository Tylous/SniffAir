#!/usr/bin/python
import argparse
from argparse import ArgumentParser, SUPPRESS, ArgumentError
import os
import subprocess


parser = argparse.ArgumentParser(usage=SUPPRESS)
parser.add_argument('-c', '--countryName', metavar='countryName', dest='countryName', action='store', help='countryName\n', required=True)
parser.add_argument('-s', '--stateOrProvinceName', metavar='stateOrProvinceName', dest='stateOrProvinceName', action='store', help='stateOrProvinceName\n', required=True)
parser.add_argument('-l', '--localityName', metavar='localityName', dest='localityName', action='store', help='localityName\n', required=True)
parser.add_argument('-o', '--organizationName', metavar='organizationName', dest='organizationName', action='store', help='organizationName\n', required=False)
parser.add_argument('-e', '--emailAddress', metavar='emailAddress', dest='emailAddress', action='store', help='emailAddress\n', required=True)
parser.add_argument('-n', '--commonName', metavar='commonName', dest='commonName', action='store', help='commonName\n', required=True)
parser.add_argument('-r', '--radius', metavar='radius', dest='radius', action='store', help='radius\n', required=True)
args = parser.parse_args()

oldfiles = "01.pem", "ca.key", "ca.pem", "dh", "index.txt", "index.txt.attr", "index.txt.old", "random", "serial", "serial.old", "server.crt", "server.key", "server.p12", "server.pem", "ca.cnf", "server.cnf", "server.csr"


for file in oldfiles:
	file = "module/hostapd-wpe/certs/" + file
	if not os.path.isfile(file):
		continue
	else:
		os.remove(file)


files = ['ca.cnf', 'server.cnf']


options = ("countryName		= " + args.countryName+ "\n"
	"stateOrProvinceName	= " + args.stateOrProvinceName + "\n"
	"localityName		= " + args.localityName + "\n"
	"organizationName	= " + args.organizationName + "\n"
	"emailAddress		= " +  args.emailAddress + "\n"
	"commonName		= " + args.commonName + "\n"
)

options1 = ("countryName         = " + args.countryName+ "\n"
        "stateOrProvinceName    = " + args.stateOrProvinceName + "\n"
        "localityName           = " + args.localityName + "\n"
        "organizationName       = " + args.organizationName + "\n"
        "emailAddress           = " +  args.emailAddress + "\n"
        "commonName             = " +  args.radius + "\n"
)


ca = '''

[ca ]

default_ca		= CA_default

[ CA_default ]
dir			= ./
certs			= $dir
crl_dir			= $dir/crl
database		= $dir/index.txt
new_certs_dir		= $dir
certificate		= $dir/server.pem
serial			= $dir/serial
crl			= $dir/crl.pem
private_key		= $dir/server.key
RANDFILE		= $dir/.rand
name_opt		= ca_default
cert_opt		= ca_default
default_days		= 365
default_crl_days	= 30
default_md		= sha256
preserve		= no
policy			= policy_match

[ policy_match ]
countryName		= match
stateOrProvinceName	= match
organizationName	= match
organizationalUnitName	= optional
commonName		= supplied
emailAddress		= optional

[ policy_anything ]
countryName		= optional
stateOrProvinceName	= optional
localityName		= optional
organizationName	= optional
organizationalUnitName	= optional
commonName		= supplied
emailAddress		= optional

[ req ]
prompt			= no
distinguished_name	= certificate_authority
default_bits		= 2048
input_password		= whatever
output_password		= whatever

[certificate_authority]

'''



server = '''

[ ca ]
default_ca		= CA_default

[ CA_default ]
dir			= ./
certs			= $dir
crl_dir			= $dir/crl
database		= $dir/index.txt
new_certs_dir		= $dir
certificate		= $dir/server.pem
serial			= $dir/serial
crl			= $dir/crl.pem
private_key		= $dir/server.key
RANDFILE		= $dir/.rand
name_opt		= ca_default
cert_opt		= ca_default
default_days		= 365
default_crl_days	= 30
default_md		= sha256
preserve		= no
policy			= policy_match

[ policy_match ]
countryName		= match
stateOrProvinceName	= match
organizationName	= match
organizationalUnitName	= optional
commonName		= supplied
emailAddress		= optional

[ policy_anything ]
countryName		= optional
stateOrProvinceName	= optional
localityName		= optional
organizationName	= optional
organizationalUnitName	= optional
commonName		= supplied
emailAddress		= optional

[ req ]
prompt			= no
distinguished_name	= server
default_bits		= 2048
input_password		= whatever
output_password		= whatever

[server]

'''


file = ca + options
outfile = open('module/hostapd-wpe/certs/ca.cnf', 'w')
outfile.write(file)
outfile.close()
file = server + options1
outfile = open('module/hostapd-wpe/certs/server.cnf', 'w')
outfile.write(file)
outfile.close()
subprocess.call('./module/hostapd-wpe/certs/bootstrap', shell=True)

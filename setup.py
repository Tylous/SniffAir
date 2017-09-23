#!/usr/bin/python

import sys
import pip
import os

os.system('apt-get update')
os.system('apt-get install dnsmasq')
os.system('apt-get install libssl1.0-dev')
os.system('apt-get install libnfnetlink-dev')
os.system('apt-get install libnl-3-dev')
os.system('apt-get install libnl-genl-3-dev')
os.system('cd module/Auto_EAP/ && python RunMeFirst.py cd ../../')


def install(package):
    pip.main(['install', package])

modules = ['pandas', 'logging', 'PrettyTable', 'tabulate', 'BaseHTTPServer', 'mimetypes']
for module in modules:
	try:
	    import module
	    print module+' is installed'
	except ImportError:
	    print module+' is not installed, installing it now!'
	    install(module)


os.system('cd module/ && tar -xvzf hostapd-2.6.tar.gz && mv hostapd-2.6/ hostapd/ && cd hostapd/ && patch -p1 < ../hostapd-wpe/hostapd-wpe.patch && cd hostapd && make') 
os.system('cd module/hostapd-wpe/certs && ./bootstrap && cd ../../')
os.system('hg clone https://bitbucket.org/secdev/scapy-com && dpkg --ignore-depends=python-scapy -r python-scapy && cd scapy-com && python setup.py install && cd ../ && rm -rf scapy-com/')


print "All Dependinces installed. Run menu.py to use SniffAir"
sys.exit(1)

#!/usr/bin/python

import sys
import pip
import threading
import subprocess
import time

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\':
                yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        sys.stdout.write('\b')
        sys.stdout.flush()
        self.busy = False
        time.sleep(self.delay)



def install(package):
    spinner = Spinner()
    spinner.start()
    pip.main(['install', package])

modules = ['pandas', 'logging', 'PrettyTable', 'scapy']
for module in modules:
	try:
	    import module
	    print module+' is installed'
	except ImportError:
	    print module+' is not installed, installing it now!'
	    install(module)



#os.system ('cd /module/ && tar -xvzf hostapd-2.6.tar.gz && cd hostapd-2.2/ && patch -p1 < ../hostapd-wpe/hostapd-wpe.patch && cd hostapd && sed -i \'s/#CONFIG_LIBNL32=y/CONFIG_LIBNL32=y/\' .config && make && cd ../../hostapd-wpe/certs && ./bootstrap && cd ../../ && rm -rf hostapd-wpe && mv hostapd-2.2/ hostapd/ ')
subprocess.Popen('cd /module/ && tar -xvzf hostapd-2.6.tar.gz && cd hostapd-2.2/ && patch -p1 < ../hostapd-wpe/hostapd-wpe.patch && cd hostapd && sed -i \'s/#CONFIG_LIBNL32=y/CONFIG_LIBNL32=y/\' .config && make && cd ../../hostapd-wpe/certs && ./bootstrap && cd ../../ && rm -rf hostapd-wpe && mv hostapd-2.2/ hostapd/' shell=True)


#os.system ('patch -p1 < ../hostapd-wpe/hostapd-wpe.patch')
#os.system ('cd hostapd')
#os.system ('sed -i \'s/#CONFIG_LIBNL32=y/CONFIG_LIBNL32=y/\' .config')
#os.system ('make')
#os.system ('cd ../../hostapd-wpe/certs')
#os.system ('./bootstrap')
#os.system ('cd ../..')
#os.system ('rm -rf hostapd-wpe')nan
#os.system ('mv hostapd-2.2/hostapd .')
#os.system ('rm -rf hostapd-2.2/')
#os.system ('rm -rf hostapd-wpe/')

#os.system('python module/Auto_EAP/RunMeFirst.py')
subprocess.Popen('python module/Auto_EAP/RunMeFirst.py', shell=True)


#os.system('hg clone https://bitbucket.org/secdev/scapy-com && dpkg --ignore-depends=python-scapy -r python-scapy && cd scapy-com && python setup.py install && cd ../ && rm -rf scapy-com/')
subprocess.Popen('hg clone https://bitbucket.org/secdev/scapy-com && dpkg --ignore-depends=python-scapy -r python-scapy && cd scapy-com && python setup.py install && cd ../ && rm -rf scapy-com/', shell=True)

#os.system('dpkg --ignore-depends=python-scapy -r python-scapy')
#os.system('cd scapy-com && python setup.py install')
#os.system('cd ../ && rm -rf scapy-com/')



spinner.stop()
print "All Dependinces installed. Run menu.py to use SniffAir"
sys.exit(1)


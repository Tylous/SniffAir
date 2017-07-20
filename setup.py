#!/usr/bin/python

import sys
import pip

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
    pip.main(['install', package])

modules = ['pandas', 'sqlite3', 'logging', 'PrettyTable', 'scapy']
for module in modules:
	try:
	    import module
	    print module+' is installed'
	except ImportError:
	    print module+' is not installed, installing it now!'
	    install(module)

spinner.start()

os.system ('cd /module/hostapd-2.2/')
os.system ('patch -p1 < ../hostapd-wpe/hostapd-wpe.patch')
os.system ('cd hostapd')
os.system ('sed -i \'s/#CONFIG_LIBNL32=y/CONFIG_LIBNL32=y/\' .config')
os.system ('make')
os.system ('cd ../../hostapd-wpe/certs')
os.system ('./bootstrap')
os.system ('cd ../..')
os.system ('rm -rf hostapd-wpe')
os.system ('mv hostapd-2.2/hostapd .')
os.system ('rm -rf hostapd-2.2/')
os.system ('rm -rf hostapd-wpe/')

spinner.stop()
sys.exit(1)


#!/usr/bin/python
import os
import os.path
import readline
import subprocess
import sys
import threading
import time

sys.path.insert(0, 'module/')
sys.path.insert(0, 'lib/')
from Sniffer import *
from Connect2DB import *
from Queries import *
import Discover_Hidden_SSID
from Discover_Hidden_SSID import *
import Suspicious_AP
from Suspicious_AP import *
import AP_Hunter
from AP_Hunter import *
import SSID_stat
import export

class colors:
	def __init__(self):
		pass

	GRN = '\033[92m'
	RD = '\033[91m'
	NRM = '\033[0m'
	BLU = '\033[34m'


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
		if delay and float(delay):
			self.delay = delay

	def spinner_task(self):
		while self.busy:
			sys.stdout.write(next(self.spinner_generator))
			sys.stdout.flush()
			time.sleep(self.delay)
			sys.stdout.write('\b')

	def start(self):
		self.busy = True
		threading.Thread(target=self.spinner_task).start()

	def stop(self):
		#sys.stdout.write('\b')
		sys.stdout.flush()
		self.busy = False
		time.sleep(self.delay)


menu_actions = {}
name = "default"
module = ""
try:
	workspace = ['workspace create', 'workspace delete', 'workspace list', 'workspace load']
	show = ['show SSIDS', 'show AP_MAC', 'show Vendor', 'show Channel', 'show Client', 'show Encrpytion', 'show Username', 'show table', 'show inscope', 'show modules', 'show inscope']
	table = ['show table AP', 'show table proberequests', 'show table proberesponses', 'show table EAP', 'show table hiddenssids', 'show table LOOT', 'show table inscope_AP', 'show table inscope_proberequests', 'show table inscope_proberesponses', ]
	modules = ['use Hidden SSID', 'use Evil Twin', 'use Captive Portal', 'use Auto EAP', 'use Auto PSK', 'use Exporter', 'use AP Hunter', 'use Suspicious AP', 'use Certificate Generator', 'use Handshaker', 'use MAC Changer', 'use Proof Packet', 'use Probe Packet', 'use Wigle Search SSID', 'use Wigle Search MAC']
	modset = ['set BSSID', 'set Channel', 'set Encryption', 'set SSID', 'set Interface', 'set WPA', 'set Key Management', 'set Password', 'set Username File', 'set Path', 'set Type', 'set PWR', 'set Country', 'set StateProvince', 'set City', 'set Client', 'set Email', 'set CommonName', 'set Server CommonName', 'set Password File', 'set APIToken', 'set APIName', 'set MAC']


	def completer(text, state):
		if text.startswith("workspace"):
			workspace_list = [x for x in workspace if x.startswith(text)]
			try:
				return workspace_list[state]
			except IndexError:
				return None
		if text.startswith("show table"):
			table_list = [x for x in table if x.startswith(text)]
			try:
				return table_list[state]
			except IndexError:
				return None
		elif text.startswith("show"):
			show_list = [x for x in show if x.startswith(text)]
			try:
				return show_list[state]
			except IndexError:
				return None
		if text.startswith("use"):
			module_list = [x for x in modules if x.startswith(text)]
			try:
				return module_list[state]
			except IndexError:
				return None
		if text.startswith("set"):
			modset_list = [x for x in modset if x.startswith(text)]
			try:
				return modset_list[state]
			except IndexError:
				return None
		else:
			options = [x for x in menu_actions if x.startswith(text)]
			try:
				return options[state]
			except IndexError:
				return None


	def choice():
		global name
		global module
		try:
			if module == "":
				readline.set_completer(completer)
				readline.set_completer_delims('')
				if 'libedit' in readline.__doc__:
					readline.parse_and_bind("bind ^I rl_complete")
				else:
					readline.parse_and_bind("tab: complete")
				raw_choice = raw_input(" >>  [" + name + "]# ")
				choice = raw_choice
				exec_menu(choice)
			else:
				readline.set_completer(completer)
				readline.set_completer_delims('')
				if 'libedit' in readline.__doc__:
					readline.parse_and_bind("bind ^I rl_complete")
				else:
					readline.parse_and_bind("tab: complete")
				raw_choice = raw_input(" >>  [" + name + "][" + module + "]# ")
				choice = raw_choice
				exec_menu(choice)
		except EOFError:
			pass
		except KeyboardInterrupt:
			exec_menu('exit')


	def main_menu():
		name = ''
		choice()
		return


	def exec_menu(choice):
		global option
		ch = choice
		if ch == '':
			menu_actions['main_menu']()
		else:
			ch1 = ch.split(' ')
			cmd = ch1[0]
			try:
				if cmd not in menu_actions:
					print colors.RD + "Invalid selection, please try again.\n" + colors.NRM
					menu_actions['main_menu']()
				else:
					option = str(ch1[1:])[1:-1].replace('\'', '').replace(",", "")
					menu_actions[cmd]()
			except AttributeError:
				menu_actions['main_menu']()
			except KeyError:
				print colors.RD + "Invalid selection, please try again.\n" + colors.NRM
				menu_actions['main_menu']()
			except IndexError:
				option = ""
				menu_actions[cmd]()
			return


	def db_check():
		if name == "default":
			print colors.RD + "Error: No workspace selected. Please create or load a workspace.\n" + colors.NRM
			menu_actions['main_menu']()
		else:
			return


	def Workspace():
		global name
		global workspace

		if option == "":
			print "     Manages workspaces"
			print " Command Option: workspaces [create|list|load|delete]"
			menu_actions['main_menu']()
		else:
			wso = option.split(' ')
			if wso[0] == "create" and wso[1] == "":
				print colors.RD + "Missing workspace name, please try again.\n" + colors.NRM
				menu_actions['main_menu']()
			if wso[0] == "create" and wso[1]:
				workspace = "db/" + wso[1] + "/" + wso[1] + ".db"
				if os.path.exists('db/' + wso[1]):
					pass
				else:
					subprocess.call('mkdir db/' + wso[1] + '', shell=True)
				Connect2DB.db_name(workspace)
				name = wso[1]
				Connect2DB.create_connection()
				print colors.GRN + "[+]" + colors.NRM + "  Workspace %s created" % (wso[1])
			if wso[0] == "load" and wso[1] == "":
				print colors.RD + "Missing workspace name, please try again.\n" + colors.NRM
				menu_actions['main_menu']()
			if wso[0] == "load" and wso[1]:
				workspace = "db/" + wso[1] + "/" + wso[1] + ".db"
				if os.path.exists('db/' + wso[1]):
					pass
				else:
					subprocess.call('mkdir db/' + wso[1] + '', shell=True)
				Connect2DB.db_name(workspace)
				name = wso[1]
				Connect2DB.create_connection()
				print colors.GRN + "[+]" + colors.NRM + " Workspace %s loaded" % (wso[1])
				d = queries()
				d.db_connect(workspace)
				IS = dp.read_sql('select * from INSCOPE_SSIDS', d.db_connect(workspace))
				if IS.empty:
					pass
				else:
					print colors.GRN + "[+] " + colors.NRM + "Inscope ESSIDs Observed"
					print dp.read_sql('select * from inscope_accessPoints', d.db_connect(workspace)).ESSID.value_counts().to_string()
				EO = dp.read_sql('select * from accessPoints', d.db_connect(workspace))
				if EO.empty:
					pass
				else:
					print colors.GRN + "[+] " + colors.NRM + "Top 5 ESSIDs Observed"
					print EO.ESSID.value_counts().head(5).to_string()
					print "\n"
				menu_actions['main_menu']()
			if wso[0] == "list":
				Connect2DB.display_list()
			if wso[0] == "delete":
				if wso[1] == "":
					print colors.RD + "Missing workspace name, please try again.\n" + colors.NRM
					menu_actions['main_menu']()
				else:
					Connect2DB.delete_workspace(wso[1])
		choice()
		exec_menu(choice)
		return


	def Live_Capture():
		db_check()
		global band
		if option == "":
			print colors.RD + "Error: No interface selected, please try again.\n" + colors.NRM
			menu_actions['main_menu']()
		else:
			try:
				global interface
				global background
				global background_thread
				background = False
				args = iter(option.split())
				interface = next(args)
				for arg in args:
					if arg == "-j":
						background = True
				c = packet_sniffer()
				if background == True:
					background_thread = threading.Thread(target=c.live_capture, args=(interface, name, workspace))
					background_thread.daemon = True
					background_thread.start()
					print colors.GRN + "[+] " + colors.NRM + "Background Thread Started"
					choice()
					exec_menu(choice)
					return
				else:
					c.live_capture(interface, name, workspace)
					print colors.GRN + "[+] " + colors.NRM + "Cleaning Up Duplicates"
					d = queries()
					d.db_connect(workspace)
					d.clean_up()
					choice()
					exec_menu(choice)
					return
			except socket.error:
				print colors.RD + "Error: Non-existant interface, please try again.\n" + colors.NRM
				choice()
				exec_menu(choice)
				return


	def Offline_Capture_List():
		global spinner
		db_check()
		if option == "":
			print colors.RD + "Error: Non-existant file, please try again.\n" + colors.NRM
			menu_actions['main_menu']()
		else:
			try:
				t = time.time()
				d = queries()
				d.db_connect(workspace)
				filepath = option
				listOfPcaps = open(filepath, 'r')
				for x in listOfPcaps:
					x = x
					spinner = Spinner()
					spinner.start()
					path = x.replace('\n', '')
					c = packet_sniffer()
					c.file(path)
					spinner.stop()
				print GRN + "[+]" + NRM + " Completed"
				print BLU + "[*]" + NRM + " Time Taken: %.3f sec" % (time.time() - t)
				d.clean_up()
				print colors.GRN + "[+] " + colors.NRM + "Cleaning Up Duplicates"
				d = queries()
				d.db_connect(workspace)
				d.clean_up()
				print colors.GRN + "[+] " + colors.NRM + "ESSIDs Observed"
				EO = dp.read_sql('select * from accessPoints', d.db_connect(workspace))
				print EO.ESSID.value_counts().to_string()
				print "\n"
			except IOError:
				spinner.stop()
				print colors.RD + "Error: Non-existant path, please try again.\n" + colors.NRM
				choice()
				exec_menu(choice)
				return
			choice()
			exec_menu(choice)
			return


	def Offline_Capture():
		db_check()
		if option == "":
			print "blah"
			print colors.RD + "Error: Non-existant file, please try again.\n" + colors.NRM
			menu_actions['main_menu']()
		else:
			try:
				t = time.time()
				spinner = Spinner()
				spinner.start()
				c = packet_sniffer()
				if option.endswith(".pcapdump"):
					path = option
					c.file(path)
				else:
					path = option
					for file in os.listdir(path):
						if file.endswith(".pcapdump"):
							fullpath = (os.path.join(path, file))
							print fullpath
							c.file(fullpath)
				spinner.stop()
				print GRN + "[+]" + NRM + " Completed"
				print BLU + "[*]" + NRM + " Time Taken: %.3f sec" % (time.time() - t)
				print colors.GRN + "[+] " + colors.NRM + "Cleaning Up Duplicates"
				d = queries()
				d.db_connect(workspace)
				d.clean_up()
				print colors.GRN + "[+] " + colors.NRM + "ESSIDs Observed"
				EO = dp.read_sql('select * from accessPoints', d.db_connect(workspace))
				print EO.ESSID.value_counts().to_string()
				print "\n"
			except IOError:
				spinner.stop()
				print colors.RD + "Error: Non-existant path, please try again.\n" + colors.NRM
				choice()
				exec_menu(choice)
				return
			choice ()
			exec_menu ( choice )
			return


	def KillSniffer():
		global background
		db_check()
		try:
			if background == True:
				background = False
				subprocess.call('killall kismet_server', shell=True)
				c = packet_sniffer()
				c.background_close()
				print colors.GRN + "[+] " + colors.NRM + "Cleaning Up Duplicates"
				d = queries()
				d.db_connect(workspace)
				d.clean_up()
				background_thread.stop()
			else:
				print "[*] Sniffer Is Not Running In The Background"
		except NameError:
			print "[*] Sniffer Is Not Running In The Background"
		choice()
		exec_menu(choice)
		return


	def SSID_Info():
		db_check()
		d = queries()
		d.db_connect(workspace)
		SSID_stat.main(workspace)
		choice()
		exec_menu(choice)
		return


	def Show():
		db_check()
		d = queries()
		d.db_connect(workspace)
		if option.startswith("table"):
			soption = option.split(' ')
			d.show_table(soption[1])
		if option.startswith("inscope"):
			result = d.show_inscope_ssids()
			print (str(result))
		if option.startswith("modules"):
			print "Available Modules"
			print "================="
			print "[+] Auto EAP - Automated Brute-Force Login Attack Against EAP Networks"
			print "[+] Auto PSK - Automated Brute-Force Passphrase Attack Against PSK Networks"
			print "[+] AP Hunter - Discover Access Point Within  a Certain Range Using a Specific Type of Encrpytion"
			print "[+] Captive Portal - Web Based Login Portal to Capture User Entered Credentials (Runs as an OPEN Network)"
			print "[+] Certificate Generator - Generates a Certificate Used by Evil Twin Attacks"
			print "[+] Exporter - Exports Data Stored in a Workspace to a CSV File"
			print "[+] Evil Twin - Creates a Fake Access Point, Clients Connect to Divulging MSCHAP Hashes or Cleartext Passwords"
			print "[+] Handshaker - Parses Database or .pcapdump Files Extracting the Pre-Shared Handshake for Password Guessing (Hashcat or JTR Format)"
			print "[+] Mac Changer - Changes The Mac Address of an Interface"
			print "[+] Probe Packet - Sends Out Deauth Packets Targeting SSID(s)"
			print "[+] Proof Packet - Parses Database or .pcapdump Files Extracting all Packets Related to the Inscope SSDIS"
			print "[+] Hidden SSID - Discovers the Names of HIDDEN SSIDS"
			print "[+] Suspicious AP - Looks for Access Points that: Is On Different Channel, use a Different Vendor or Encrpytion Type Then the Rest of The Network"
			print "[+] Wigle Search SSID - Queries wigle for SSID (i.e. Bob's wifi)"
			print "[+] Wigle Search MAC - Queries wigle for all observations of a single mac address"
		d.show(option)
		choice()
		exec_menu(choice)
		return


	def inscope():
		db_check()
		d = queries()
		d.db_connect(workspace)
		d.in_scope(option)
		choice()
		exec_menu(choice)
		return


	def Query():
		db_check()
		if option == "":
			print colors.RD + "Error: Invalid query, please try again.\n" + colors.NRM
			menu_actions['main_menu']()
		else:
			d = queries()
			d.db_connect(workspace)
			d.Custom_Queries(option)
			choice()
			exec_menu(choice)
			return


	def clear():
		os.system('clear')
		choice()
		exec_menu(choice)
		return


	def Help():
		print "Commands"
		print "========"
		print "workspace                Manages workspaces (create, list, load, delete)"
		print "live_capture             Initiates a valid wireless interface to collect wireless pakcets to be parsed (requires the interface name)"
		print "offline_capture          Begins parsing wireless packets using a pcap file-kismet .pcapdump work best (requires the full path)"
		print "offline_capture_list     Begins parsing wireless packets using a list of pcap file-kismet .pcapdump work best (requires the full path)"
		print "query                    Executes a query on the contents of the acitve workspace"
		print "help                     Displays this help menu"
		print "clear                    Clears the screen"
		print "show                     Shows the contents of a table, specific information across all tables or the available modules"
		print "inscope                  Add ESSID to scope. inscope [ESSID]"
		print "SSID_Info                Displays all information (i.e all BSSID, Channels and Encrpytion) related to the inscope SSIDS"
		print "use                      Use a SniffAir module"
		print "info                     Displays all variable information regarding the selected module"
		print "set                      Sets a variable in module"
		print "exploit                  Runs the loaded module"
		print "run                      Runs the loaded module"
		print "exit                     Exit SniffAir"
		choice()
		exec_menu(choice)
		return


	def exit():
		print "\n"
		print "Good Bye..."
		sys.exit()


	def info():
		if module == "":
			print colors.RD + "Error: No module selected, please select one.\n" + colors.NRM
		else:
			print "Globally Set Varibles"
			print "====================="
			try:
				if (list1['Module']) in ["Evil Twin"]:
					print " Module: " + (list1['Module'])
					print " Interface: " + (list1['Interface']) + "          The Interface to Use"
					print " SSID: " + (list1['SSID']) + "          The SSID to Masquerade As"
					print " Channel: " + (list1['Channel']) + "          The Channel for the AP to be on"
					print " WPA Version: " + (list1['WPA']) + "          The WPA Version to use"
					print " Type: " + (list1['Type']) + "          Either MSCHAP or GTC"
					print " Background: " + (list1['Type']) + "          Run Evil AP in the background"
				if (list1['Module']) in ["Captive Portal"]:
					print " Module: " + (list1['Module'])
					print " Interface: " + (list1['Interface']) + "          The Interface to Use"
					print " SSID: " + (list1['SSID']) + "          The SSID to Masquerade As"
					print " Channel: " + (list1['Channel']) + "          The Channel for the AP to be on"
					print " Template: Cisco (More to be added soon)"
				if (list1['Module']) in ["Auto EAP"]:
					print " Module: " + (list1['Module'])
					print " Interface: " + (list1['Interface']) + "          The Interface to Use"
					print " SSID: " + (list1['SSID']) + "          The SSID To Target"
					print " Encryption: " + (list1['Encryption']) + "          EAP Encryption Type (Default: PEAP)"
					print " Key Management: " + (list1['Key_Management']) + "          The Type of Key Management Used (Default: WPA-EAP)"
					print " Password: " + (list1['Password']) + "          The Password to Use"
					print " Username File: " + (list1['Username_File'])
				if (list1['Module']) in ["Auto PSK"]:
					print " Module: " + (list1['Module'])
					print " Interface: " + (list1['Interface']) + "          The Interface to Use"
					print " SSID: " + (list1['SSID']) + "          The SSID To Target"
					print " Password File: " + (list1['PasswordFile']) + "          The file of Potential Passwords"
				if (list1['Module']) in ["Exporter"]:
					print " Module: " + (list1['Module'])
					print " Path: " + (list1['Path']) + "          The Path to store the Generated CSV file"
				if (list1['Module']) in ["Certificate Generator"]:
					print " Module: " + (list1['Module'])
					print " Country: " + (list1['Country']) + "          The first 2 letters of the country"
					print " StateProvince: " + (list1['StateProvince']) + "          The name of state or province"
					print " City: " + (list1['City']) + "          The name of the city"
					print " Client: " + (list1['Client']) + "          The name of the client"
					print " Email: " + (list1['Email']) + "          The assoicated email address for the certificate (ex. admin@acme.com)"
					print " CommonName: " + (list1['CommonName']) + "          The CommonName (ex. ca.acme.com)"
					print " Server CommonName: " + (list1['ServerCommonName']) + "          The radius server's CommonName (ex. radius.acme.com)"
				if (list1['Module']) in ["Handshaker"]:
					print " Module: " + (list1['Module'])
					print " Format: " + (list1['Format']) + "          The type of Output for Offline Password Guessing (Hashcat or JTR)"
					print " SSID: " + (list1['SSID']) + "          A specific SSID to Parse for (If left Blank, will use the ones in the Inscope Field)"
					print " Path: " + (list1['Path']) + "          The Path to store the Generate the File (Default is db/workspace/)"
					print " Input File: " + (list1['InputFile']) + "          a .pcapdump file to parse"
				if (list1['Module']) in ["MAC Changer"]:
					print " Module: " + (list1['Module'])
					print " Interface: " + (list1['Interface']) + "          The Interface to Change the MAC of"
					print " MAC: " + (list1['MAC']) + "          The MAC Address to Change to"
				if (list1['Module']) in ["Proof Packet"]:
					print " Module: " + (list1['Module'])
					print " SSID: " + (list1['SSID']) + "          A specific SSID to Parse for (If left Blank, will use the ones in the Inscope Field)"
					print " Path: " + (list1['Path']) + "          The Path to store the Generate the Filtered.cap File (Default is db/workspace/)"
				if (list1['Module']) in ["Probe Packet"]:
					print " Module: " + (list1['Module'])
					print " Interface: " + (list1['Interface']) + "          The Interface to Use"
					print " Count: " + (list1['Count']) + "          How many Packets to Send (0 means Unlimited)"
					print " Delay: " + (list1['Delay']) + "          How long to wait before the next Request"
					print " MAC: " + (list1['MAC']) + "          MAC Address to Target a Specific Client or AP (Optional)"
					print " SSID: " + (list1['SSID']) + "          The SSID to Deauth"
					print " SSID File: " + (list1['InputFile']) + "          The Containing a List of SSID to Deauth (Optional)"
				if (list1['Module']) in ["Wigle Search SSID"]:
                                        print " Module: " + (list1['Module'])
                                        print " APIName: " + (list1['APIName']) + "          Wigle API Name"
                                        print " APIToken: " + (list1['APIToken']) + "          Wigle API Token"
                                        print " SSID: " + (list1['SSID']) + "          SSID to query"
				if (list1['Module']) in ["Wigle Search MAC"]:
                                        print " Module: " + (list1['Module'])
                                        print " APIName: " + (list1['APIName']) + "          Wigle API Name"
                                        print " APIToken: " + (list1['APIToken']) + "          Wigle API Token"
                                        print " MAC: " + (list1['MAC']) + "          MAC address to query"
			except NameError:
				pass
		choice()
		exec_menu(choice)
		return


	def use():
		if option == "":
			print colors.RD + "Missing Module name, please try again.\n" + colors.NRM
			menu_actions['main_menu']()
		else:
			global module
			global list1
			list1 = {'Module': '', 'Interface': '', 'SSID': '', 'BSSID': '', 'Channel': '', 'Encryption': 'PEAP', 'WPA': '', 'Key_Management': 'WPA-EAP', 'Password': '', 'Username_File': '', 'Type': '', 'Country': '', 'StateProvince': '', 'City': '', 'Client': '', 'Email': '', 'CommonName': '', 'ServerCommonName': '', 'PasswordFile': '', 'Path': '', 'Format': '', 'MAC': '', 'InputFile': '', 'Delay': '', 'Count': '', 'APIName': '', 'APIToken': ''}
			if option in ["Evil Twin"]:
				module = option
				list1.update(Module=module)
			elif option in ["Captive Portal"]:
				module = option
				list1.update(Module=module)
			elif option in ["Auto EAP"]:
				module = option
				list1.update(Module=module)
			elif option in ["Hidden SSID"]:
				module = option
				list1.update(Module=module)
				Discover_Hidden_SSID.main(workspace)
			elif option in ["Exporter"]:
				module = option
				list1.update(Module=module)
			elif option in ["Suspicious AP"]:
				module = option
				list1.update(Module=module)
				Suspicious_AP.main(workspace)
			elif option in ["AP Hunter"]:
				module = option
				list1.update(Module=module)
				AP_Hunter.main(workspace)
			elif option in ["Certificate Generator"]:
				module = option
				list1.update(Module=module)
			elif option in ["Auto PSK"]:
				module = option
				list1.update(Module=module)
			elif option in ["Handshaker"]:
				module = option
				list1.update(Module=module)
			elif option in ["MAC Changer"]:
				module = option
				list1.update(Module=module)
			elif option in ["Proof Packet"]:
				module = option
				list1.update(Module=module)
			elif option in ["Probe Packet"]:
				module = option
				list1.update(Module=module)
			elif option in ["Wigle Search SSID"]:
                                module = option
                                list1.update(Module=module)
			elif option in ["Wigle Search MAC"]:
                                module = option
                                list1.update(Module=module)
			else:
				print colors.RD + "Error: Non-existant module, please try again.\n" + colors.NRM
		choice()
		exec_menu(choice)
		return


	def set():
		if module == "":
			print colors.RD + "Missing Module name, please try again.\n" + colors.NRM
			menu_actions['main_menu']()
		else:
			varibles = option.split(' ')
			if varibles[0] == "":
				print "Missing Varibles name, please try again.\n"
				menu_actions['main_menu']()
			try:
				if varibles[0] in ["BSSID"]:
					global bssid
					list1.update(BSSID=varibles[1])
					bssid = varibles[1]
				if varibles[0] in ["Channel"]:
					global channel
					list1.update(Channel=varibles[1])
				if varibles[0] in ["Encryption"]:
					global encryption
					list1.update(Encryption=varibles[1])
				if varibles[0] in ["Interface"]:
					global interface
					interface = varibles[1]
					list1.update(Interface=varibles[1])
				if varibles[0] in ["WPA"]:
					global wpa
					list1.update(WPA=varibles[1])
				if varibles[0] + ' ' + varibles[1] in ["Key Management"]:
					global Key_MGT
					list1.update(Key_Management=varibles[2])
				if varibles[0] in ["Password"]:
					global password
					list1.update(Password=varibles[1])
				if varibles[0] + ' ' + varibles[1] in ["Username File"]:
					global Username_File
					list1.update(Username_File=varibles[2])
				if varibles[0] in ["Path"]:
					global Path
					list1.update(Path=varibles[1])
				if varibles[0] in ["Type"]:
					global Type
					list1.update(Type=varibles[1])
				if varibles[0] in ["Country"]:
					global Country
					list1.update(Country=varibles[1])
				if varibles[0] in ["StateProvince"]:
					global StateProvince
					list1.update(StateProvince=varibles[1])
				if varibles[0] in ["City"]:
					global City
					list1.update(City=varibles[1])
				if varibles[0] in ["Client"]:
					global Client
					varibles = " ".join(varibles[1:])
					list1.update(Client=varibles)
				if varibles[0] in ["Email"]:
					global Email
					list1.update(Email=varibles[1])
				if varibles[0] in ["CommonName"]:
					global commonName
					list1.update(CommonName=varibles[1])
				if varibles[0] + ' ' + varibles[1] in ["Server CommonName"]:
					global ServerCommonName
					list1.update(ServerCommonName=varibles[2])
				if varibles[0] + ' ' + varibles[1] in ["Password File"]:
					global PasswordFile
					list1.update(PasswordFile=varibles[2])
				if varibles[0] in ["Path"]:
					global path
					path = varibles[1]
					list1.update(Path=varibles[1])
				if varibles[0] in ["Format"]:
					global format
					format = varibles[1]
					list1.update(Format=varibles[1])
				if varibles[0] in ["MAC"]:
					global MAC
					MAC = varibles[1]
					list1.update(MAC=varibles[1])
				if varibles[0] in ["APIName"]:
                                        global APIName
                                        APIName = varibles[1]
                                        list1.update(APIName=varibles[1])
				if varibles[0] in ["APIToken"]:
                                        global APIToken
                                        APIToken = varibles[1]
                                        list1.update(APIToken=varibles[1])
				if varibles[0] in ["Count"]:
					global Count
					Count = varibles[1]
					list1.update(Count=varibles[1])
				if varibles[0] in ["Delay"]:
					global Delay
					Delay = varibles[1]
					list1.update(Delay=varibles[1])
				if varibles[0] + ' ' + varibles[1] in ["Input File"]:
					global InputFile
					list1.update(InputFile=varibles[2])
				if varibles[0] + ' ' + varibles[1] in ["SSID File"]:
					global InputFile
					list1.update(InputFile=varibles[2])
				elif varibles[0] in ["SSID"]:
					global ssid
					varibles = " ".join(varibles[1:])
					list1.update(SSID=varibles)
			except NameError:
				pass
			choice()
			exec_menu(choice)
			return


	def exploit():
		if module == "":
			print colors.RD + "No module selected, please try again.\n" + colors.NRM
			menu_actions['main_menu']()
		else:
			try:
				if module in ['Hidden SSID']:
					d = queries()
					d.db_connect(workspace)
					Discover_Hidden_SSID.main(workspace)
				if module in ['AP Hunter']:
					d = queries()
					d.db_connect(workspace)
					AP_Hunter.main(workspace)
				if module in ['Exporter']:
					d = queries()
					d.db_connect(workspace)
					export.main(workspace, list1['Path'], name)
				if module in ['Evil Twin']:
					if list1['SSID'] and list1['Channel'] and list1['Interface'] and list1['Type']:
						if list1['Type'] == "GTC":
							args = ' -s "' + list1['SSID'] + '" -c ' + list1['Channel'] + ' -a \'Evil Twin\' -w ' + list1['WPA'] + ' -i ' + list1['Interface'] + ' -g ' + list1['Type'] + ' -d ' + workspace + ''
						else:
							args = ' -s "' + list1['SSID'] + '" -c ' + list1['Channel'] + ' -a \'Evil Twin\' -w ' + list1['WPA'] + ' -i ' + list1['Interface'] + ' -d ' + workspace + ''
						os.system('python module/hostapd.py' + args + '')
					else:
						print "Error: Invalid or Missing Arguements"
				if module in ['Captive Portal']:
					if list1['SSID'] and list1['Channel'] and list1['Interface']:
						args = ' -s "' + list1['SSID'] + '" -c ' + list1['Channel'] + ' -a \'Captive Portal\' -i ' + list1['Interface'] + ' -d ' + workspace + ''
						os.system('python module/hostapd.py' + args + '')
					else:
						print "Error: Invalid or Missing Arguements"
				if module in ['Auto EAP']:
					if list1['SSID'] and list1['Key_Management'] and list1['Encryption'] and list1['Password'] and list1['Interface']:
						if not list1['Username_File']:
							args = ' -s "' + list1['SSID'] + '" -K ' + list1['Key_Management'] + ' -E ' + list1['Encryption'] + ' -W ' + workspace + ' -p ' + list1['Password'] + ' -i ' + list1['Interface']
						else:
							print list1['Password']
							args = ' -s "' + list1['SSID'] + '" -K ' + list1['Key_Management'] + ' -E ' + list1['Encryption'] + ' -U ' + list1['Username_File'] + ' -p \'' + list1['Password'] + '\' -i ' + list1['Interface'] + ' -W ' + workspace + ''
							print args
						os.system('cd module/Auto_EAP/ && python Auto_EAP.py' + args + '&& cd ../../')
					else:
						print "Error: Invalid or Missing Arguements"
				if module in ['Certificate Generator']:
					if list1['Country'] and list1['StateProvince'] and list1['City'] and list1['Client'] and list1['Email'] and list1['CommonName'] and list1['ServerCommonName']:
						args = ' -c ' + list1['Country'] + ' -s ' + list1['StateProvince'] + ' -l ' + list1['City'] + ' -o "' + list1['Client'] + '" -e ' + list1['Email'] + ' -n ' + list1['CommonName'] + ' -r ' + list1['ServerCommonName']
						os.system('python module/hostapd-wpe/certs/cert.py ' + args + '')
					else:
						print "Error: Invalid or Missing Arguements"
				if module in ['Auto PSK']:
					if list1['SSID'] and list1['PasswordFile'] and list1['Interface']:
						args = ' -s "' + list1['SSID'] + '" -W ' + workspace + ' -P \'' + list1['PasswordFile'] + '\' -i ' + list1['Interface']
						os.system('cd module/Auto_EAP/ && python Auto_PSK.py' + args + '&& cd ../../')
					else:
						print "Error: Invalid or Missing Arguements"
				if module in ['Handshaker']:
					if list1['Format']:
						if list1['SSID']:
							ssid_args = ' -s ' + list1['SSID']
						else:
							ssid_args = ""
						if list1['Path']:
							path_args = ' -p ' + list1['Path']
						else:
							path_args = ""
						if list1['InputFile']:
							IF_args = ' -I ' + list1['InputFile']
						else:
							IF_args = ""
						args = ' -w ' + workspace + ' -f ' + list1['Format'] + ssid_args + path_args + IF_args
						os.system('cd module/Handshaker/ && python Handshaker.py' + args + '&& cd ../../')
					else:
						print "Error: Invalid or Missing Arguements"
				if module in ['MAC Changer']:
					if list1['MAC'] and list1['Interface']:
						args = ' -I ' + list1['Interface'] + ' -M ' + list1['MAC']
						os.system('cd module/ && python MAC_Changer.py' + args + '&& cd ../../')
					else:
						print "Error: Invalid or Missing Arguements"
				if module in ['Proof Packet']:
					if workspace == "default":
						print "Error: Invalid or Missing Arguements"
						return
					else:
						args = ' -W ' + str(workspace)
					if list1['SSID']:
						args = args + ' -S ' + list1['SSID']
					else:
						print "Error: Invalid or Missing Arguements"
						return
					if list1['Path']:
						args = args + ' -P ' + list1['Path']
						os.system('cd module/ && python proof_packet.py' + args + '&& cd ../../')
					else:
						os.system('cd module/ && python proof_packet.py' + args + '&& cd ../../')
				if module in ['Probe Packet']:
					args = ' -i ' + list1['Interface'] + ' -d ' + list1['Delay'] + ' -c ' + list1['Count']
					if list1['MAC']:
						args = args + ' -m ' + list1['MAC']
					else:
						print "Error: Invalid or Missing Arguements"
						return
					if list1['SSID']:
						args = args + ' -s ' + list1['SSID']
						os.system('cd module/ && python Probe_Packet.py' + args + '&& cd ../../')
					elif list1['SSID File']:
						args = args + ' -f ' + list1['InputFile']
						os.system('cd module/ && python Probe_Packet.py' + args + '&& cd ../../')
					else:
						print "Error: Invalid or Missing Arguements"
				if module in ['Wigle Search SSID']:
					args = ''
                                        if list1['APIName'] and list1['APIToken'] and list1['SSID']:
                                                args = ' ' + list1['APIName'] + ' ' + list1['APIToken'] + ' ' + list1['SSID']
                                                os.system('cd module/ && python wigleSearchESSID.py' + args + '&& cd ../../')
                                        else:
                                                print "Error: Invalid or Missing Arguements"
				if module in ['Wigle Search MAC']:
                                        args = ''
					if list1['APIName'] and list1['APIToken'] and list1['MAC']:
						args = ' ' + list1['APIName'] + ' ' + list1['APIToken'] + ' ' + list1['MAC']
                                                os.system('cd module/ && python wigleSearchBSSID.py' + args + '&& cd ../../')
                                        else:
                                                print "Error: Invalid or Missing Arguements"
			except KeyboardInterrupt:
				pass
		choice()
		exec_menu(choice)
		return


	# =======================
	#   Menu Options
	# =======================

	menu_actions = {'main_menu': main_menu, 'workspace': Workspace, 'offline_capture_list': Offline_Capture_List, 'live_capture': Live_Capture, 'offline_capture': Offline_Capture, 'help': Help, 'show': Show, 'Query': Query, 'SSID_Info': SSID_Info, 'inscope': inscope, 'query': Query, 'set': set, 'info': info, 'clear': clear, 'exploit': exploit, 'run': exploit, 'use': use, 'exit': exit, 'KillSniffer': KillSniffer, }

except Exception:
	pass


def banner():
	f = open('banner', 'r')
	print f.read()
	f.close()


if __name__ == "__main__":
	banner()
	print "\n"
	if len(sys.argv) > 1:
		ws = sys.argv[1]
		if os.path.exists('db/' + ws + '/' + ws + '.db'):
			exec_menu('workspace load ' + ws)
		else:
			exec_menu('workspace create ' + ws)
	main_menu()

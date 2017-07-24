#!/usr/bin/python
import sys
sys.path.insert(0, 'module/')
sys.path.insert(0, 'lib/')
import os, signal
from Sniffer import *
from Connect2DB import *
import time
import threading
from Queries import *
import Discover_Hidden_SSID
import SSID_stat


class colors:
    GRN = '\033[92m'
    RD = '\033[91m'
    NRM = '\033[0m'

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

menu_actions  = {}
name = "default"
module = ""
try:
    def choice():
        global name
        global module
        try:
            if module == "":
                raw_choice = raw_input(" >>  [" + name + "]# ")
                choice = raw_choice
                exec_menu(choice)
            else:
                raw_choice = raw_input(" >>  [" + name + "][" + module + "]# ")
                choice = raw_choice
                exec_menu(choice)
        except EOFError:
            pass
        except KeyboardInterrupt:
            exec_menu('exit')

    # Main menu
    def main_menu():

        name = ''
        choice()
        return
     
    # Execute menu
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
                    option = str(ch1[1:])[1:-1].replace('\'', '').replace(",","")
                    menu_actions[cmd]()
            except KeyError:
                print colors.RD + "Invalid selection, please try again.\n" + colors.NRM
                menu_actions['main_menu']()
            except IndexError:
                option = ""
                menu_actions[cmd]()
            return


    def Create_Workspace():
        global name
        global workspace
        if option == "":
            print colors.RD + "Missing workspace name, please try again.\n" + colors.NRM 
            menu_actions['main_menu']()
        else: 
            workspace = "db/" + option + ".db"
            Connect2DB.db_name(workspace)
            name = option
            Connect2DB.create_connection()
            print colors.GRN + "[+]"+ colors.NRM +"  Workspace %s created" % (option)
            choice()
            exec_menu(choice)
        
     
     
    def Load_Workspace():
        if option == "":
            print colors.RD + "Missing workspace name, please try again.\n" + colors.NRM 
            menu_actions['main_menu']()
        else: 
            global name
            global workspace
            workspace = "db/" + option + ".db"
            Connect2DB.db_name(workspace)
            name = option
            Connect2DB.create_connection()
            print colors.GRN + "[+]"+ colors.NRM +" Workspace %s loaded" % (option)
            d = queries()
            d.db_connect(workspace)
            print "[+] ESSIDs Observed"
            EO = dp.read_sql('select * from accessPoints', d.db_connect(workspace))
            print EO.ESSID.value_counts().to_string()
            print "\n"
            choice()
            exec_menu(choice)
        
        

    def Live_Packet():
        if option == "":
            print colors.RD + "Error: Non-existant interface, please try again.\n" + colors.NRM 
            menu_actions['main_menu']()
        else: 
            global interface
            name = "db/" + option + ".db"
            Connect2DB.db_name(name)
            workspace = option
            c = packet_sniffer()
            c.live_capture(interface)
            d = queries()
            d.db_connect(workspace)
            d.clean_up()
            print "[+] ESSIDs Observed"
            EO = dp.read_sql('select * from accessPoints', d.db_connect(workspace))
            print EO.ESSID.value_counts()
            print "\n"
            choice()
            exec_menu(choice)
            return

    def Offline_Capture_List():
        if option == "":
            print colors.RD + "Error: Non-existant file, please try again.\n" + colors.NRM 
            menu_actions['main_menu']()
        else:
            try:
                spinner = Spinner()
                spinner.start() 
                d = queries()
                d.db_connect(workspace)
                filepath = option
                listOfPcaps = open(filepath, 'r')
                for x in listOfPcaps:
                    x = x[:-1]
                    path = x
                    c = packet_sniffer()
                    c.file(path)
                    spinner.stop() 
                    print "[+] Cleaning Up Duplicates"
                    d.db_connect(workspace)
                    print "[+] ESSIDs Observed"
                    EO = dp.read_sql('select * from accessPoints', d.db_connect(workspace))
                    print EO.ESSID.value_counts().to_string()
                    print "\n"
                d.clean_up()
            except IOError:
                spinner.stop()
                print colors.RD + "Error: Non-existant path, please try again.\n" + colors.NRM
            choice()
            exec_menu(choice)
            return 

    def Offline_Capture():
        if option == "":
            print colors.RD + "Error: Non-existant file, please try again.\n" + colors.NRM 
            menu_actions['main_menu']()
        else:
            try:
                spinner = Spinner()
                spinner.start() 
                path = option
                c = packet_sniffer()
                c.file(path)
                spinner.stop() 
                print "[+] Cleaning Up Duplicates"
                d = queries()
                d.db_connect(workspace)
                d.clean_up()
                print "[+] ESSIDs Observed"
                EO = dp.read_sql('select * from accessPoints', d.db_connect(workspace))
                print EO.ESSID.value_counts().to_string()
                print "\n"
                choice()
                exec_menu(choice)
                return    
            except IOError:
                spinner.stop()
                print colors.RD + "Error: Non-existant path, please try again.\n" + colors.NRM
                choice()
                exec_menu(choice)
                return   

    def SSID_Info():
        d = queries()
        d.db_connect(workspace)
        SSID_stat.main(workspace)
        choice()
        exec_menu(choice)
        return

    def Run_Hidden_SSID():
        d = queries()
        d.db_connect(workspace)
        Discover_Hidden_SSID.main(workspace)
        choice()
        exec_menu(choice)
        return

    def show_table():
        d = queries()
        d.db_connect(workspace)
        d.show_table(option)
        choice()
        exec_menu(choice)
        return

    def Show():
        d = queries()
        d.db_connect(workspace)
        d.show(option)
        choice()
        exec_menu(choice)
        return

    def inscope():
        d = queries()
        d.db_connect(workspace)
        d.in_scope(option)
        choice()
        exec_menu(choice)
        return

    def show_inscope():
        d = queries()
        d.db_connect(workspace)
        result = d.show_inscope_ssids()
        print (str(result))
        choice()
        exec_menu(choice)
        return

    def Show_Modules():
        print "Show Modules"
        print "[+] Hidden SSID"
        print "[+] Evil Twin"
        print "[+] Captive Portal"
        print "[+] Auto_EAP"
        print "[+] Network Mapper"
        choice()
        exec_menu(choice)
        return

    def Query():
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

    def Help():#missing hidden ssid and ssid info hostapd etc
        print "Commands"
        print "========"
        print "create_workspace         Creates a new workspace"
        print "load_workspace           Loads an existing workspace"
        print "live_capture             Initiates an valid wireless interface to collect wireless pakcets to be parsed (requires the interface name)"
        print "offline_capture          begins parsing wireless packets using an pcap file-kistmit .pcapdump work best (requires the full path)"
        print "offline_capture_list     begins parsing wireless packets using an list of pcap file-kistmit .pcapdump work best (requires the full path)"
        print "query                    Executes a quey on the contents of the acitve workspace"
        print "help                     Displays this help menu"
        print "show                     shows specific information from all tables"
        print "show_table               shows a specific tables in db"
        print "inscope                  add ESSID to scope. inscope [ESSID]"
        print "show_Modules             Show SniffAir modules"
        print "use_module               Use a SniffAir module"
        print "info                     Displays all varible infomraiton regardin the selected module"
        print "set                      Sets a varible in module"
        print "exploit                  Runs the loaded module"
        print "exit                     Exit SniffAir"
        choice()
        exec_menu(choice)
        return

    def exit():
        print "\n"
        print "Good Bye..."
        sys.exit()

    def info():
        print "Globally Set Varibles"
        try:
            if (list1['Module']) in ["Evil Twin"]:
                print " Module: "+(list1['Module'])
                print " Interface: "+(list1['Interface'])
                print " SSID: "+(list1['SSID'])
                print " Channel: "+(list1['Channel'])
                print " WPA Version: "+(list1['WPA'])
            if (list1['Module']) in ["Captive Portal"]:
                print " Module: "+(list1['Module'])
                print " Interface: "+(list1['Interface'])
                print " SSID: "+(list1['SSID'])
                print " Channel: "+(list1['Channel'])
                print " WPA Version: "+(list1['WPA'])
            if (list1['Module']) in ["Auto EAP"]:
                print " Module: "+(list1['Module'])
                print " Interface: "+(list1['Interface'])
                print " SSID: "+(list1['SSID'])
                print " Encryption: "+(list1['Encryption'])
                print " Key Management: "+(list1['Key_Management'])
                print " Password: "+(list1['Password'])
                print " Username File: "+(list1['Username_File'])
        except NameError:
            pass
        choice()
        exec_menu(choice)
        return


    def use_module():
        if option == "":
            print colors.RD + "Missing workspace name, please try again.\n" + colors.NRM 
            menu_actions['main_menu']()
        else:
            global module 
            global list1
            list1 = {'Module': '','Interface': '','SSID': '','BSSID': '','Channel': '','Encryption': '','WPA': '','Key_Management': '','Password': '', 'Username_File': ''}
            if option in ["Evil Twin"]:
                module = option
                list1.update(Module = module)
            elif option in ["Captive Portal"]:
                module = option
                list1.update(Module = module)
            elif option in ["Auto EAP"]:
                module = option
                list1.update(Module = module)
            else:
                print colors.RD + "Error: Non-existant module, please try again.\n" + colors.NRM 
        choice()
        exec_menu(choice) 
        return


    def set():
        varibles = option.split(' ')
        if varibles[0] == "":
            print "Missing workspace name, please try again.\n" 
            menu_actions['main_menu']()
        try:
            if varibles[0] in ["BSSID"]:
                global bssid
                list1.update(BSSID = varibles[1])
                bssid = varibles[1]
            if varibles[0] in ["Channel"]:
                global channel
                list1.update(Channel = varibles[1])
            if varibles[0] in ["Encryption"]:
                global encryption
                list1.update(Encryption = varibles[1])
            if varibles[0] in ["SSID"]:
                global ssid
                list1.update(SSID = varibles[1])
            if varibles[0] in ["Interface"]:
                global interface
                interface = varibles[1]
                list1.update(Interface = varibles[1])
            if varibles[0] in ["WPA"]:
                global wpa
                list1.update(WPA = varibles[1])
            if varibles[0] in ["Key_Management"]:
                global Key_MGT 
                list1.update(Key_Management = varibles[1])
            if varibles[0] in ["Password"]:
                global password
                list1.update(Password = varibles[1])
            if varibles[0] in ["Username_File"]:
                global Username_File
                list1.update(Username_File = varibles[1])
        except NameError:
            pass    
        choice()
        exec_menu(choice)
        return

    def exploit(): 
        if module == "":
            print colors.RD + "No module selected, please try again.\n" + colors.NRM 
            menu_actions['main_menu']()
            global p
        else:
            try:
                if module in ['Evil Twin']:
                    args = ' -s '+ list1['SSID']+' -c '+ list1['Channel'] +' -a \'Evil Twin\' -w '+ list1['WPA']+' -i '+ list1['Interface']+''
                    os.system('python module/hostapd.py'+args+'')  
                if module in ['Captive Portal']:
                    args = ' -s '+ list1['SSID']+' -c '+ list1['Channel'] +' -a \'Captive Portal\' -w '+ list1['WPA']+' -i '+ list1['Interface']+''
                    os.system('python module/hostapd.py' +args+'')
                if module in ['Auto EAP']:
                    if not list1['Username_File']:
                        args = ' -s '+ list1['SSID']+' -K '+ list1['Key_Management'] +' -E '+list1['Encryption'] +' -W '+workspace+' -p '+ list1['Password']+' -i '+ list1['Interface']+''
                    else:
                        args = ' -s '+ list1['SSID']+' -K '+ list1['Key_Management'] +' -E '+list1['Encryption'] +' -U '+list1['Username_File']+' -p '+ list1['Password']+' -i '+ list1['Interface']+''
                    os.system('cd module/Auto_EAP/ && python Auto_EAP.py' +args+'&& cd ../../')
            except KeyboardInterrupt:
                pass
        choice()
        exec_menu(choice)
        return
     
    # =======================
    #   Menu Options
    # =======================

    menu_actions = {
        'main_menu': main_menu,
        'offline_capture_list': Offline_Capture_List,
        'create_workspace': Create_Workspace,
        'load_workspace': Load_Workspace,
        'live_packet': Live_Packet,
        'offline_capture': Offline_Capture,
        'help': Help,
        'show' : Show,
        'Query' : Query,
        'Run_Hidden_SSID': Run_Hidden_SSID,
        'SSID_Info' : SSID_Info,
        'show_inscope' : show_inscope,
        'inscope' : inscope,
        'show_table' : show_table,
        'query' : Query,
        'set' : set,
        'info' : info,
        'clear' : clear,
        'exploit' : exploit,
        'use_module': use_module,
        'show_modules': Show_Modules,
        'exit': exit,
    }

     
except Exception:
    pass
def banner():
    f = open('banner', 'r')
    print f.read()
    f.close()

if __name__ == "__main__":
    banner()
    print "\n"
    main_menu()

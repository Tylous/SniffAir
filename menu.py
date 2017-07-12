
#!/usr/bin/python

import sys
import os
from Sniffer import *
from Connect2DB import *
import time
import sys
import os
import colorama
from ConfigParser import SafeConfigParser
from Queries import *
import Queries

class colors:
    GRN = '\033[92m'
    RD = '\033[91m'
    NRM = '\033[0m'


menu_actions  = {}
workspace = "default"

def choice():
    global workspace
    try:
        raw_choice = raw_input(" >>  [" + workspace + "]# ")
        choice = raw_choice
        exec_menu(choice)
    except KeyboardInterrupt:
        exec_menu('exit')

    

# Main menu
def main_menu():

    workspace = ''
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
    global workspace
    if option == "":
        print colors.RD + "Missing workspace name, please try again.\n" + colors.NRM 
        menu_actions['main_menu']()
    else: 
        name = option
        Connect2DB.db_name(name)
        workspace = Connect2DB.db_file
        Connect2DB.create_connection()
        print colors.GRN + "[+]"+ colors.NRM +"  Workspace %s created" % (option)
        choice()
        exec_menu(choice)
    
 
 
def Load_Workspace():
    if option == "":
        print colors.RD + "Missing workspace name, please try again.\n" + colors.NRM 
        menu_actions['main_menu']()
    else: 
        global workspace
        name = option
        Connect2DB.db_name(name)
        workspace = Connect2DB.db_file
        Connect2DB.create_connection()
        print colors.GRN + "[+]"+ colors.NRM +" Workspace %s loaded" % (option)
        choice()
        exec_menu(choice)
    
    

def Live_Packet():
    if option == "":
        print colors.RD + "Error: Non-existant interface, please try again.\n" + colors.NRM 
        menu_actions['main_menu']()
    else: 
        print "live Capture"
        interface = option
        print option
        c = packet_sniffer()
        c.live_capture(interface)
        clean1.clean_up(workspace)
        choice()
        exec_menu(choice)
        return

def Offline_Capture():
    #pdb.set_trace()
    if option == "":
        print colors.RD + "Error: Non-existant file, please try again.\n" + colors.NRM 
        menu_actions['main_menu']()
    else: 
        path = option
        c = packet_sniffer()
        c.file(path)
        print "[+] Cleaning Up Duplicates"
        d = queries()
        d.db_connect(workspace)
        d.clean_up()
        choice()
        exec_menu(choice)
        return

def show_table():
    #clean1.show_table(workspace, option)
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
    #clean1.show(workspace, option)
    choice()
    exec_menu(choice)
    return

def inscope():
    d = queries()
    Queries.inscope.append(option)
    d.db_connect(workspace)
    d.in_scope(option)

    #clean1.show(workspace, option)
    choice()
    exec_menu(choice)
    return


def Query():
    if option == "":
        print colors.RD + "Error: Invalid query, please try again.\n" + colors.NRM 
        menu_actions['main_menu']()
    else: 
        print "Query DB"
        q = Query()
        print option
        connect_db()
        q.show()
        return

def Show_Modules():
    print "Show Modules"
    print "[+] Hidden SSID"
    print "[+] Evil Twin"
    print "[+] Auto_EAP"
    print "[+] Take Over the World"
    print "[+] Launch Nuke"
    print "[+] Get Bacon"
    choice()
    exec_menu(choice)
    return

def Load():
    print "Load Modules"
    choice()
    exec_menu(choice)
    return

def Help():
    print "Commands"
    print "========"
    print "create_workspace         Creates a new workspace"
    print "load_workspace           Loads an existing workspace"
    print "live_capture             Initiates an valid wireless interface to collect wireless pakcets to be parsed (requires the interface name)"
    print "offline_capture          beings parsing wireless packets using an pcap file-kistmit .pcapdump work best (requires the full path)"
    print "query                    Execute a quey on the contents of the acitve workspace"
    print "show_Modules             Show SniffAir modules"
    print "use_module               Use a SniffAir module"
    print "exit                     Exit SniffAir"
    choice()
    exec_menu(choice)
    return

def exit():
    print "\n"
    print "Good Bye..."
    sys.exit()


 
# =======================
#   Menu Options
# =======================

menu_actions = {
    'main_menu': main_menu,
    'create_workspace': Create_Workspace,
    'load_workspace': Load_Workspace,
    'live_packet': Live_Packet,
    'offline_capture': Offline_Capture,
    'help': Help,
    'show' : Show,
    'inscope' : inscope,
    'show_table' : show_table,
    'query' : Query,
    'load' : Load,
    'show_modules': Show_Modules,
    'exit': exit,
}

 

def banner():
    f = open('banner', 'r')
    print f.read()
    f.close()

if __name__ == "__main__":
    banner()
    print "\n"
    main_menu()

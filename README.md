# SniffAir

SniffAir is an open-source wireless security framework. Sniffair allows for the collection, management, and analysis of wireless traffic. In additional, SniffAir can also be used to preform sophisticated wireless attacks. SniffAir was born out of the hassle of managing large or multiple pcap files while thoroughly cross-examining and analyzing the traffic, looking for potential security flaws or malicious traffic. 

SniffAir is developed by [@Tyl0us](https://twitter.com/Tyl0us) and [@theDarracott](https://twitter.com/theDarracott)


## Install
-----
To install run the setup.py script
```
$python setup.py
```

## Usage
-----

```

                                                                     % *        ., %                         
                                                                    % ( ,#     (..# %                        
    /@@@@@&,    *@@%        &@,    @@#    /@@@@@@@@@   .@@@@@@@@@. ,/ # # (%%%* % (.(.  .@@     &@@@@@@%.    
  .@@&   *&@    %@@@@.      &@,    @@%    %@@,,,,,,,   ,@@,,,,,,,  .( % %  %%#  # % #   ,@@     @@(,,,#@@@.  
  %@%           %@@(@@.     &@,    @@%    %@@          ,@@          /* #   /*,   %.,,   ,@@     @@*     #@@  
  ,@@&          %@@ ,@@*    &@,    @@%    %@@          ,@@           .#   //#(,   (,    ,@@     @@*     &@%  
   .@@@@@.      %@@  .@@(   &@,    @@%    %@@%%%%%%*   ,@@%%%%%%#         (# ##.        ,@@     @@&%%%@@@%   
       *@@@@    %@@   .@@/  &@,    @@%    %@@,,,,,,    ,@@,,,,,,.        %#####%        ,@@     @@(,,%@@%    
          @@%   %@@     @@( &@,    @@%    %@@          ,@@              %  (*/  #       ,@@     @@*    @@@   
          %@%   %@@      @@&&@,    @@%    %@@          ,@@             %  #  .# .#      ,@@     @@*     @@%  
 .@@&/,,#@@@    %@@       &@@@,    @@%    %@@          ,@@            /(*       /(#     ,@@     @@*      @@# 
   *%@@@&*      *%#        ,%#     #%/    *%#           %%            #############.    .%#     #%.      .%% 
                                                                  (@Tyl0us & @theDarracott)

 >>  [default]# help
Commands
========
workspace                Manages workspaces (create, list, load, delete)
live_capture             Initiates an valid wireless interface to collect wireless packets to be parsed (requires the interface name)
offline_capture          Begins parsing wireless packets using an pcap file-kistmit .pcapdump work best (requires the full path)
offline_capture_list     Begins parsing wireless packets using an list of pcap file-kistmit .pcapdump work best (requires the full path)
query                    Executes a quey on the contents of the acitve workspace
help                     Displays this help menu
clear                    Clears the screen
show                     Shows the contents of a table, specific information accorss all tables or the avilable modules
inscope                  Add ESSID to scope. inscope [ESSID]
use                      Use a SniffAir module
info                     Displays all varible infomraiton regardin the selected module
set                      Sets a varible in module
exploit                  Runs the loaded module
exit                     Exit SniffAir
 >>  [default]# 
```

## Begin
-----
First create or load a new or existing workspace using the command ```workspace create <workspace>``` or ```workspace load <workspace>``` command. To view all existing workspaces use the ```workspace list``` command and ```workspace delete <workspace>``` command to delete the desired workspace:
 
```
 >>  [default]# workspace
     Manages workspaces
 Command Option: workspaces [create|list|load|delete]
>>  [default]# workspace create demo
[+]  Workspace demo created
```


Load data into a desired workplace from a pcap file using the command ```offline_capture <the full path to the pcap file>```. To load a series of pcap files use the command ```offline_capture_list <the full path to the file containing the list of pcap name>``` (this file should contain the full patches to each pcap file).
 
 ```
 >>  [demo]# offline_capture /root/sniffair/demo.pcapdump
\
[+] Completed
[+] Cleaning Up Duplicates
[+] ESSIDs Observed
```
 

## Show Command
-----
The ```show``` command displays the contents of a table, specific information across all tables or the available modules, using the following syntax:

```
 >>  [demo]# show table AP
+------+-----------+-------------------+-------------------------------+--------+-------+-------+----------+--------+
|   ID | ESSID     | BSSID             | VENDOR                        |   CHAN |   PWR | ENC   | CIPHER   | AUTH   |
|------+-----------+-------------------+-------------------------------+--------+-------+-------+----------+--------|
|    1 | HoneyPot  | c4:6e:1f:0c:82:03 | TP-LINK TECHNOLOGIES CO. LTD. |      4 |   -17 | WPA2  | TKIP     | MGT    |
|    2 | Demo      | 80:2a:a8:5a:fb:2a | Ubiquiti Networks Inc.        |     11 |   -19 | WPA2  | CCMP     | PSK    |
|    3 | Demo5ghz  | 82:2a:a8:5b:fb:2a | Unknown                       |     36 |   -27 | WPA2  | CCMP     | PSK    |
|    4 | HoneyPot1 | c4:6e:1f:0c:82:05 | TP-LINK TECHNOLOGIES CO. LTD. |     36 |   -29 | WPA2  | TKIP     | PSK    |
|    5 | BELL456   | 44:e9:dd:4f:c2:7a | Sagemcom Broadband SAS        |      6 |   -73 | WPA2  | CCMP     | PSK    |
+------+-----------+-------------------+-------------------------------+--------+-------+-------+----------+--------+
 >>  [demo]# show SSIDS
---------
HoneyPot
Demo
HoneyPot1
BELL456
Hidden
Demo5ghz
---------

```

The ```query``` command can be used to display a unique set of data based on the parememters specificed. The ```query``` command uses sql syntax.

## Modules
-----

Modules can be used to analyze the data contained in the workspaces or preform offensive wireless attacks using the ```use <module name>``` command. For some modules additional variables may need to be set. They can be set using the set command ```set <variable name> <variable value>```:
```
 >>  [demo]# show modules
Available Modules
[+] Run Hidden SSID
[+] Evil Twin
[+] Captive Portal
[+] Auto EAP
[+] Exporter
 >>  [demo]# 
 >>  [demo]# use Captive Portal
 >>  [demo][Captive Portal]# info
Globally Set Varibles
=====================
 Module: Captive Portal
 Interface: 
 SSID: 
 Channel: 
 Template: Cisco (More to be added soon)
 >>  [demo][Captive Portal]# set Interface wlan0
 >>  [demo][Captive Portal]# set SSID demo
 >>  [demo][Captive Portal]# set Channel 1
 >>  [demo][Captive Portal]# info
Globally Set Varibles
=====================
 Module: Captive Portal
 Interface: wlan0
 SSID: demo
 Channel: 1
 Template: Cisco (More to be added soon)
 >>  [demo][Captive Portal]# 
```
Once all varibles are set, then execute the exploit command to run the desired attack.


## Export
-----
To export all information stored in a workspace’s tables using the ```Exporter``` module and setting the desired path.

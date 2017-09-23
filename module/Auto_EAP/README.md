# Auto_EAP

## Introduction
-----
######Published Sepetember 15, 2016

Auto_EAP.py is a script designed to perform automated brute-force authentication attacks against various types of EAP networks. These types of wireless networks provide an interface to facilitate password guessing of domain credentials as radius servers check authentication against Active Directory. Using the python library wpaspy, created by [Jouni Malinen <j@w1.fi>] (https://github.com/jmalinen/hostap/tree/master/wpaspy)
to interact with the wpa_supplicant daemon, automated authentication attacks can be preformed with the intent of not causing account lock-outs. 

## Demo
-----

```
./Auto_EAP.py -s HoneyPot -K WPA-EAP -E PEAP -U test.txt -p Summer2016 -i wlan0
Initialized...
Trying Username Alice with Password test: SUCCESS
Trying Username Bob with Password test: FAILED
Trying Username Charles with Password test: FAILED
Trying Username David with Password test: SUCCESS
Completed

```

## Installation
-----

Run 'RunMeFirst.py' within the root directory of Auto_EAP. This will compile the wpaspy library as well as setup a stand alone wpa_supplicant.conf file that Auto_EAP.py will use for testing, leaving the system’s wpa_supplicant config file untouched.  

## Help
-----

```
./Auto_EAP.py -h
usage: Auto_EAP.py [-h] -i Interface -s SSID -U Usernamefile -p Password -K
                   Key_mgmt -E Eap_type

optional arguments:
  -h, --help            show this help message and exit
  -i Interface, --interface Interface
                        The Interface to use
  -s SSID, --ssid SSID  The SSID to attack
  -U Usernamefile, --User Usernamefile
                        Path to username file
  -p Password, --password Password
                        Password to use
  -K Key_mgmt, --key_mgmt Key_mgmt
                        Key_Management type to use
  -E Eap_type, --eap_type Eap_type
                        Eap type to use

```

## Todo list
-----
* [✓] Resoved bug  with .a type wireless cards (Shout out to [Havok0x90] (https://twitter.com/havok0x90) for his help in resolving this issue)
* [-] Add multi-threading functionality
* [-] Add support for password lists



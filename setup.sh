#!/bin/bash
if lsb_release -d | grep -q "Kali"
then
	Release=Kali
	apt-get update -y
	apt-get install -y dnsmasq libssl1.0-dev libnfnetlink-dev libnl-3-dev libnl-genl-3-dev wireshark tcpdump python-setuptools ca-certificates git make wget gcc pkg-config libnl-3-dev
        easy_install pip
	pushd module/Auto_EAP/
	python RunMeFirst.py
	popd
	pushd module/
	wget https://w1.fi/releases/hostapd-2.6.tar.gz
	tar -xzf hostapd-2.6.tar.gz
	mv hostapd-2.6/ hostapd/
	rm -rf hostapd-2.6.tar.gz
	pushd hostapd/
	patch -p1 < ../hostapd-wpe/hostapd-wpe.patch
	pushd hostapd
	make
	popd
	popd
	pushd hostapd-wpe/certs
	./bootstrap
	popd
	popd
elif lsb_release -d | grep -q "Ubuntu"
then
	Release=Ubuntu
	apt-get update -y
	apt-get install -y dnsmasq libssl-dev libnfnetlink-dev libnl-3-dev libnl-genl-3-dev wireshark tcpdump python-setuptools ca-certificates git make wget gcc pkg-config libnl-3-dev
        easy_install pip
	pushd module/Auto_EAP/
	python RunMeFirst.py
	popd
	pushd module/
	wget https://w1.fi/releases/hostapd-2.6.tar.gz
	tar -xzf hostapd-2.6.tar.gz
	mv hostapd-2.6/ hostapd/
	rm -rf hostapd-2.6.tar.gz
	pushd hostapd/
	patch -p1 < ../hostapd-wpe/hostapd-wpe.patch
	pushd hostapd
	make
	popd
	popd
	pushd hostapd-wpe/certs
	./bootstrap
	popd
	popd
elif lsb_release -d | grep -q "Debian"
then
	Release=Debian
	apt-get update -y
	apt-get install -y dnsmasq libssl1.0-dev libnfnetlink-dev libnl-3-dev libnl-genl-3-dev build-essential gcc wireshark tcpdump python-setuptools ca-certificates git make wget libnl-3-dev pkg-config
        easy_install pip
	pushd module/Auto_EAP/
	python RunMeFirst.py
	popd
	pushd module/
	wget https://w1.fi/releases/hostapd-2.6.tar.gz
	tar -xzf hostapd-2.6.tar.gz
	mv hostapd-2.6/ hostapd/
	rm -rf hostapd-2.6.tar.gz
	pushd hostapd/
	patch -p1 < ../hostapd-wpe/hostapd-wpe.patch
	pushd hostapd/
	make
	popd
	popd
	pushd hostapd-wpe/certs
	./bootstrap
	popd
	popd
else
	echo -ne "Unknown/Unsupported Distro\n"
	echo -ne "Quiting...\n"
	exit 1
fi

rm -rf db/.keep

echo -ne "Below are is the contents of the requirement, if you wish to install them please enter yes. Note that SniffAir will not run properly without them.\n"
echo -ne "[*] pandas\n"
echo -ne "[*] logging\n"
echo -ne "[*] PrettyTable\n"
echo -ne "[*] tabulate\n"
echo -ne "[*] BaseHTTPServer\n"
echo -ne "[*] mimetypes\n"
echo -ne "[*] scapy 2.3.3\n"
echo -n "Do you wish to install these program? [y/n]"
read answer
if echo "$answer" | grep -iq "^y" ;then

	pip install pandas
	pip install logging
	pip install PrettyTable
	pip install tabulate
	pip install BaseHTTPServer
	pip install mimetypes
	pip install git+https://github.com/secdev/scapy
	echo -e "[+]All Dependinces installed. Run SniffAir.py to use SniffAir\n"
else :
	echo -e "[-] ERROR: Dependinces not installed. SniffAir will not beable to run until they are install\n"
	exit 1

fi


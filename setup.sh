#!/bin/bash
if lsb_release -d | grep -q "Kali"
then
	Release=Kali
	apt-get update -y
	apt-get install -y dnsmasq libssl1.0-dev libnfnetlink-dev libnl-genl-3-dev wireshark tcpdump python-setuptools ca-certificates git make wget gcc pkg-config libnl-3-dev
        easy_install pip
	pushd module/Auto_EAP/
	python RunMeFirst.py
	popd
	pushd module/
	wget ftp://ftp.freeradius.org/pub/radius/old/freeradius-server-2.1.12.tar.bz2
	tar -jxvf freeradius-server-2.1.12.tar.bz2
	mv freeradius-server-2.1.12 freeradius
	rm -rf freeradius-server-2.1.12.tar.bz2
	pushd freeradius
	patch -p1 < ../gtc/PuNk1n.patch
	./configure
	make
	make install
	ldconfig
	mv /usr/local/etc/raddb/eap.conf /usr/local/etc/raddb/eap.conf.bak
	mv ../gtc/eap.conf /usr/local/etc/raddb/eap.conf
	mv /usr/local/etc/raddb/clients.conf /usr/local/etc/raddb/clients.conf.bak
	mv ../gtc/clients.conf /usr/local/etc/raddb/clients.conf
	popd
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
	apt-get install -y dnsmasq libssl-dev libnfnetlink-dev libnl-genl-3-dev wireshark tcpdump python-setuptools ca-certificates git make wget gcc pkg-config libnl-3-dev
        easy_install pip
	pushd module/Auto_EAP/
	python RunMeFirst.py
	popd
	pushd module/
		pushd module/Auto_EAP/
	python RunMeFirst.py
	popd
	pushd module/
	wget ftp://ftp.freeradius.org/pub/radius/old/freeradius-server-2.1.12.tar.bz2
	tar -jxvf freeradius-server-2.1.12.tar.bz2
	mv freeradius-server-2.1.12 freeradius
	rm -rf freeradius-server-2.1.12.tar.bz2
	pushd freeradius
	patch -p1 < ../gtc/PuNk1n.patch
	./configure
	make
	make install
	ldconfig
	mv /usr/local/etc/raddb/eap.conf /usr/local/etc/raddb/eap.conf.bak
	mv ../gtc/eap.conf /usr/local/etc/raddb/eap.conf
	mv /usr/local/etc/raddb/clients.conf /usr/local/etc/raddb/clients.conf.bak
	mv ../gtc/clients.conf /usr/local/etc/raddb/clients.conf
	popd
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
elif lsb_release -d | grep -q "Gentoo"
then
	Release=Gentoo
	emerge --sync
	emerge --oneshot portage
	emerge net-dns/dnsmasq dev-vcs/git net-misc/wget net-analyzer/wireshark net-analyzer/tcpdump app-misc/ca-certificates sys-devel/make sys-devel/gcc dev-util/pkgconfig dev-libs/libnl dev-python/setuptools net-libs/libnfnetlink dev-libs/openssl dev-python/pip
	pushd module/Auto_EAP/
	python RunMeFirst.py
	popd
	pushd module/
		pushd module/Auto_EAP/
	python RunMeFirst.py
	popd
	pushd module/
	wget ftp://ftp.freeradius.org/pub/radius/old/freeradius-server-2.1.12.tar.bz2
	tar -jxvf freeradius-server-2.1.12.tar.bz2
	mv freeradius-server-2.1.12 freeradius
	rm -rf freeradius-server-2.1.12.tar.bz2
	pushd freeradius
	patch -p1 < ../gtc/PuNk1n.patch
	./configure
	make
	make install
	ldconfig
	mv /usr/local/etc/raddb/eap.conf /usr/local/etc/raddb/eap.conf.bak
	mv ../gtc/eap.conf /usr/local/etc/raddb/eap.conf
	mv /usr/local/etc/raddb/clients.conf /usr/local/etc/raddb/clients.conf.bak
	mv ../gtc/clients.conf /usr/local/etc/raddb/clients.conf
	popd
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
	apt-get install -y dnsmasq libssl1.0-dev libnfnetlink-dev libnl-genl-3-dev build-essential gcc wireshark tcpdump python-setuptools ca-certificates git make wget libnl-3-dev pkg-config
        easy_install pip
	pushd module/Auto_EAP/
	python RunMeFirst.py
	popd
	pushd module/
		pushd module/Auto_EAP/
	python RunMeFirst.py
	popd
	pushd module/
	wget ftp://ftp.freeradius.org/pub/radius/old/freeradius-server-2.1.12.tar.bz2
	tar -jxvf freeradius-server-2.1.12.tar.bz2
	mv freeradius-server-2.1.12 freeradius
	rm -rf freeradius-server-2.1.12.tar.bz2
	pushd freeradius
	patch -p1 < ../gtc/PuNk1n.patch
	./configure
	make
	make install
	ldconfig
	mv /usr/local/etc/raddb/eap.conf /usr/local/etc/raddb/eap.conf.bak
	mv ../gtc/eap.conf /usr/local/etc/raddb/eap.conf
	mv /usr/local/etc/raddb/clients.conf /usr/local/etc/raddb/clients.conf.bak
	mv ../gtc/clients.conf /usr/local/etc/raddb/clients.conf
	popd
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
echo -ne "[*] scapy\n"
echo -ne "[*] gmplot\n"
echo -ne "[*] requests\n"
echo -n "Do you wish to install these python modules? [y/n]"
read answer
if echo "$answer" | grep -iq "^y" ;then


	pip2 install -r requirements.txt --user
	echo -e "[+]All Dependencies installed. Run SniffAir.py to use SniffAir\n"
else :
	echo -e "[-] ERROR: Dependencies not installed. SniffAir will not be able to run until they are installed\n"
	exit 1

fi



FROM python:2.7-stretch
RUN apt-get update && apt-get upgrade -y
RUN apt-get install git aircrack-ng tcpdump libnl-3-dev dnsmasq libssl1.0-dev libnfnetlink-dev libnl-genl-3-dev screen wireshark kismet -y
RUN git clone https://github.com/Tylous/SniffAir.git
WORKDIR /SniffAir/module/Auto_EAP/
RUN python RunMeFirst.py
WORKDIR /SniffAir/
RUN python2 -m pip install pandas logging PrettyTable tabulate twisted mime mimetype-match
WORKDIR /SniffAir/module/
RUN  tar -xvzf hostapd-2.6.tar.gz && mv hostapd-2.6/ hostapd/ && cd hostapd/ && patch -p1 < ../hostapd-wpe/hostapd-wpe.patch && cd hostapd && make
WORKDIR /SniffAir/module/hostapd-wpe/certs/
RUN ./bootstrap
WORKDIR /SniffAir/
RUN hg clone https://bitbucket.org/secdev/scapy-com
RUN dpkg --ignore-depends=python-scapy -r python-scapy
WORKDIR /SniffAir/scapy-com/
RUN python2 setup.py install
WORKDIR /SniffAir/
ENTRYPOINT ["python2","/SniffAir/SniffAir.py"]

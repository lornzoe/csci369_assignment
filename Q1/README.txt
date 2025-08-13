Q1 - ARP Spoofer
----------------
This program performs an ARP spoofing attack.

Requirements:
- Kali VM (as attacker)
	- Python installed
	- Scapy installed
	- sudo/root privileges (required for sending raw packets)
- Metasploitable2 (as victim)

Usage:
	sudo python3 arpspoof.py <Victim_IP> <Router_IP>

Example:
	sudo python3 arpspoof.py 10.0.2.4 10.0.2.1
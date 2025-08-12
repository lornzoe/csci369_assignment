Q1 - ARP Spoofer
----------------
This program performs an ARP spoofing attack.

Before usage, ensure IP forwarding is enabled on the Kali VM.
	echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

Requirements:
- Kali VM (as attacker)
	- Python installed
	- Scapy installed
- Metasploitable2 (as victim)

Usage:
	sudo python3 arpspoof.py <Victim_IP> <Router_IP>

Example:
	sudo python3 arpspoof.py 10.0.2.4 10.0.2.1
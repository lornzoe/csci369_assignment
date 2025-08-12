Q2 - Cookie Stealer
-------------------

Requirements:
- Kali VM (attacker)
	- python installed (python3)
	- python-venv installed (python3-venv)
	- Flask (to be installed in the virtual environment)
- Metasploitable2 VM (victim)

Usage:
	1) Flask app:
	- Run on Kali VM
		- Note: Make sure your Kali VM firewall allows incoming connections on port 5000.
			sudo ufw allow 5000
			sudo ufw reload
		- Set up & activate the virtual environment to run Flask in, if it isn't yet:
			python3 -m venv .venv
			. .venv/bin/activate
			pip install Flask
	- Run the app while in the virtual environment:
		flask --app cookiestealer run

	The app listens on port 5000 and logs stolen cookies with timestamps in cookies.txt

	2) JavaScript payload:
	- Run Metasploitable2 VM (for DVWA)
		- On Kali VM:
		- Replace <KALI_IP> in xss_payload.txt with your Kali VM IP
		- Go to DVWA (http://<Meta2_IP>/DVWA) on Kali
		- Set security to "medium"
		- Navigate to "XSS Reflected"
		- Insert the JS snippet from xss_payload.txt into "What's your name" field
		- Submit it

	3) When victim loads the page with injected JS, their cookie will be sent to the Flask app and logged.

---


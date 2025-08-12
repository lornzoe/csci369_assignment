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
		- Ensure port 5000 can allow incoming connections.
		- Activate the virtual environment
			. .venv/bin/activate
	- Run the app while in the virtual environment:
		python3 cookiestealer.py

	2) JavaScript payload:
	- Run Metasploitable2 VM (for DVWA)
	- On Kali VM:
		- Replace <KALI_IP> in xss_payload.txt with your Kali VM IP
		- Go to DVWA (http://<META2_IP>/dvwa) on Kali and log in (admin/password)
		- Navigate to Security
			- Set security to "low" 
		- Navigate to "XSS Reflected"
			- Insert the JS snippet from xss_payload.txt into "What's your name" field
			- Submit

	The app listens on port 5000 and logs stolen cookies with timestamps in cookies.txt
	When a victim loads the page with injected JS, their cookie will be sent to the Flask app and be logged in both console and cookies.txt.

---


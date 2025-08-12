Q2 - Cookie Stealer

1) Flask app:

- Run on Kali VM
- Setup virtual environment & install Flask:
	sudo apt install python3.12-venv
	python3.12 -m venv myproject
	source myproject/bin/activate
	pip install flask
- Run the app:
  python app.py

- The app listens on port 5000 and logs stolen cookies with timestamps in cookies.txt

2) JavaScript payload:

- Replace <KALI_IP> in xss_payload.txt with your Kali VM IP
- Go to DVWA (http://<Meta2_IP>/DVWA) on Kali or any browser
- Set security to "medium"
- Navigate to "XSS Reflected"
- Insert the JS snippet from xss_payload.txt into "What's your name" field
- Submit it

3) When victim loads the page with injected JS, their cookie will be sent to the Flask app and logged.

---

Note: Make sure your Kali VM firewall allows incoming connections on port 5000.

Q3 - Ransomware
---------------
Requirements:
    - Kali VM (victim machine)

1. generate key to key.txt
2. generate public/private key pair for the attacker
3. encrypt my_secretes.txt using key.txt to data_cipher.txt
4. encrypt key.txt to with public key to key_cipher.txt
5. delete key.txt and my_secrets.txt
6. display message
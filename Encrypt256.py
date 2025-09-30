#USAGE EXAMPLE
#
#To encrypt a file: Encrypt256.py encrypt --file FileName.pdf 
# (Enter and remember the password.)
#
#To decrypt a file: Encrypt256.py decrypt --file Filename.pdf.enc
# (Enter the password you remembered.)
#
#This Python script uses AES-256-CBC to encrypt any file passed to it at the bit level, utilizing HMAC-SHA256 
#to confirm that the file hasn't been altered. The key is derived from your password with PBKDF2 with an embedded salt.
#PKCS7 padding is used for files that don't perfectly align with 16-byte blocks.
#
#!/usr/bin/env python3

import argparse
import sys
import os
from pathlib import Path
import base64
import hashlib
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from getpass import getpass

def generate_key_and_iv(password: str, salt: bytes = None) -> tuple[bytes, bytes, bytes]:
    """Generate AES-256 key, IV, and HMAC key from password using PBKDF2."""
    if salt is None:
        salt = os.urandom(16)  # Random 16-byte salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=80,  # 32 (AES-256 key) + 16 (IV) + 32 (HMAC key)
        salt=salt,
        iterations=100000,
    )
    derived = kdf.derive(password.encode('utf-8'))
    aes_key = derived[:32]  # First 32 bytes for AES-256
    iv = derived[32:48]     # Next 16 bytes for IV
    hmac_key = derived[48:] # Last 32 bytes for HMAC
    return aes_key, iv, hmac_key, salt

def encrypt_file(file_path: Path, password: str, output_dir: Path = None) -> Path:
    """Encrypt a file with AES-256-CBC and HMAC-SHA256, embedding salt."""
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        print(f"[INFO] Read file: {file_path}")

        aes_key, iv, hmac_key, salt = generate_key_and_iv(password)
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
        encryptor = cipher.encryptor()

        # Pad data to multiple of 16 bytes
        pad_length = 16 - (len(data) % 16)
        padded_data = data + bytes([pad_length] * pad_length)

        # Encrypt
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Compute HMAC
        h = hmac.HMAC(hmac_key, hashes.SHA256())
        h.update(ciphertext)
        hmac_tag = h.finalize()

        # Combine salt, ciphertext, and HMAC
        encrypted = salt + ciphertext + hmac_tag

        # Write to output file
        output_file = output_dir / f"{file_path.name}.enc" if output_dir else file_path.with_suffix(file_path.suffix + '.enc')
        with open(output_file, 'wb') as f:
            f.write(encrypted)
        print(f"[INFO] Encrypted file saved: {output_file}")
        print(f"[INFO] Salt is embedded in the encrypted file. Only the password is needed for decryption.")
        return output_file
    except Exception as e:
        print(f"[ERROR] Encryption failed: {e}", file=sys.stderr)
        sys.exit(1)

def decrypt_file(file_path: Path, password: str, output_dir: Path = None) -> Path:
    """Decrypt a file with AES-256-CBC and verify HMAC-SHA256, extracting embedded salt."""
    try:
        with open(file_path, 'rb') as f:
            encrypted = f.read()
        print(f"[INFO] Read encrypted file: {file_path}")

        # Extract salt (first 16 bytes), ciphertext, and HMAC (last 32 bytes)
        salt = encrypted[:16]
        ciphertext = encrypted[16:-32]
        received_hmac = encrypted[-32:]

        aes_key, iv, hmac_key, _ = generate_key_and_iv(password, salt)

        # Verify HMAC
        h = hmac.HMAC(hmac_key, hashes.SHA256())
        h.update(ciphertext)
        h.verify(received_hmac)
        print(f"[INFO] HMAC verification passed")

        # Decrypt
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        # Remove padding
        pad_length = padded_data[-1]
        decrypted = padded_data[:-pad_length]

        # Write to output file
        output_file = output_dir / f"{file_path.name}.dec" if output_dir else file_path.with_suffix('')
        with open(output_file, 'wb') as f:
            f.write(decrypted)
        print(f"[INFO] Decrypted file saved: {output_file}")
        return output_file
    except Exception as e:
        print(f"[ERROR] Decryption failed: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Encrypt/decrypt any file with AES-256-CBC and HMAC-SHA256.")
    parser.add_argument('action', choices=['encrypt', 'decrypt'], help="Action to perform")
    parser.add_argument('--file', type=Path, required=True, help="File to encrypt/decrypt")
    parser.add_argument('--output-dir', type=Path, help="Directory for output files (default: same as input)")
    
    args = parser.parse_args()

    if not args.file.is_file():
        print(f"[ERROR] File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    password = getpass("[INPUT] Enter password: ")
    if not password:
        print("[ERROR] Password cannot be empty", file=sys.stderr)
        sys.exit(1)

    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.action == 'encrypt':
        encrypt_file(args.file, password, args.output_dir)
    elif args.action == 'decrypt':
        decrypt_file(args.file, password, args.output_dir)

if __name__ == '__main__':
    main()
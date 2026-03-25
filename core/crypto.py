"""
Hardened encryption module using AES-256-GCM with Argon2 key derivation
End-to-end encryption for cleaned images
"""

import os
import json
from typing import Tuple, Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2.low_level import hash_secret_raw, Type
import secrets
import base64


class ImageCrypto:
    """
    Military-grade encryption for scrubbed images
    Uses AES-256-GCM with Argon2id key derivation
    """

    # Argon2 parameters (hardened)
    ARGON2_TIME_COST = 4          # Iterations
    ARGON2_MEMORY_COST = 2**16    # 64 MB
    ARGON2_PARALLELISM = 4        # Threads
    ARGON2_HASH_LEN = 32          # 256 bits
    ARGON2_SALT_LEN = 32          # 256 bits

    # AES-GCM parameters
    AES_KEY_SIZE = 32             # 256 bits
    AES_NONCE_SIZE = 12           # 96 bits (recommended for GCM)
    AES_TAG_SIZE = 16             # 128 bits

    def __init__(self, verbose: bool = True):
        """
        Initialize encryption engine

        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose

    def derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Derive encryption key from password using Argon2id

        Args:
            password: User password
            salt: Random salt

        Returns:
            Derived 256-bit key
        """
        if self.verbose:
            print("[*] Deriving encryption key with Argon2id...")

        key = hash_secret_raw(
            secret=password.encode('utf-8'),
            salt=salt,
            time_cost=self.ARGON2_TIME_COST,
            memory_cost=self.ARGON2_MEMORY_COST,
            parallelism=self.ARGON2_PARALLELISM,
            hash_len=self.ARGON2_HASH_LEN,
            type=Type.ID  # Argon2id (hybrid)
        )

        if self.verbose:
            print("[+] Key derivation complete")

        return key

    def encrypt_file(self, input_path: str, output_path: str,
                    password: str, metadata: Optional[dict] = None) -> bool:
        """
        Encrypt a file with AES-256-GCM

        Args:
            input_path: Path to file to encrypt
            output_path: Path to save encrypted file
            password: Encryption password
            metadata: Optional metadata to embed (already scrubbed data info)

        Returns:
            Success status
        """
        try:
            if self.verbose:
                print(f"[*] Encrypting: {os.path.basename(input_path)}")

            # Read plaintext
            with open(input_path, 'rb') as f:
                plaintext = f.read()

            # Generate salt and nonce
            salt = secrets.token_bytes(self.ARGON2_SALT_LEN)
            nonce = secrets.token_bytes(self.AES_NONCE_SIZE)

            # Derive key
            key = self.derive_key(password, salt)

            # Initialize AES-GCM
            aesgcm = AESGCM(key)

            # Prepare associated data (metadata)
            if metadata:
                associated_data = json.dumps(metadata).encode('utf-8')
            else:
                associated_data = b'ImageGhost-v3.0'

            # Encrypt
            ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)

            # Build encrypted container
            container = {
                'version': 1,
                'algorithm': 'AES-256-GCM',
                'kdf': 'Argon2id',
                'salt': base64.b64encode(salt).decode('utf-8'),
                'nonce': base64.b64encode(nonce).decode('utf-8'),
                'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
                'metadata': metadata or {}
            }

            # Write encrypted container
            with open(output_path, 'w') as f:
                json.dump(container, f, indent=2)

            if self.verbose:
                print(f"[+] Encrypted: {os.path.basename(output_path)}")
                print(f"    Original size: {len(plaintext):,} bytes")
                print(f"    Encrypted size: {len(ciphertext):,} bytes")

            # Securely clear sensitive data
            del plaintext
            del key
            del ciphertext

            return True

        except Exception as e:
            if self.verbose:
                print(f"[-] Encryption failed: {str(e)}")
            return False

    def decrypt_file(self, input_path: str, output_path: str,
                    password: str) -> Tuple[bool, Optional[dict]]:
        """
        Decrypt a file encrypted with encrypt_file

        Args:
            input_path: Path to encrypted file
            output_path: Path to save decrypted file
            password: Decryption password

        Returns:
            Tuple of (success, metadata)
        """
        try:
            if self.verbose:
                print(f"[*] Decrypting: {os.path.basename(input_path)}")

            # Read encrypted container
            with open(input_path, 'r') as f:
                container = json.load(f)

            # Validate version
            if container.get('version') != 1:
                raise ValueError("Unsupported container version")

            # Extract components
            salt = base64.b64decode(container['salt'])
            nonce = base64.b64decode(container['nonce'])
            ciphertext = base64.b64decode(container['ciphertext'])
            metadata = container.get('metadata', {})

            # Derive key
            key = self.derive_key(password, salt)

            # Initialize AES-GCM
            aesgcm = AESGCM(key)

            # Prepare associated data
            if metadata:
                associated_data = json.dumps(metadata).encode('utf-8')
            else:
                associated_data = b'ImageGhost-v3.0'

            # Decrypt
            plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data)

            # Write decrypted file
            with open(output_path, 'wb') as f:
                f.write(plaintext)

            if self.verbose:
                print(f"[+] Decrypted: {os.path.basename(output_path)}")
                print(f"    Size: {len(plaintext):,} bytes")

            # Securely clear sensitive data
            del plaintext
            del key

            return True, metadata

        except Exception as e:
            if self.verbose:
                print(f"[-] Decryption failed: {str(e)}")
            return False, None

    def batch_encrypt(self, input_dir: str, output_dir: str,
                     password: str, file_list: Optional[list] = None) -> dict:
        """
        Batch encrypt multiple files

        Args:
            input_dir: Input directory
            output_dir: Output directory
            password: Encryption password
            file_list: Optional list of specific files

        Returns:
            Statistics dictionary
        """
        os.makedirs(output_dir, exist_ok=True)

        if file_list is None:
            file_list = os.listdir(input_dir)

        stats = {'success': 0, 'failed': 0}

        print(f"\n[*] Encrypting {len(file_list)} files...")
        print("=" * 60)

        for idx, filename in enumerate(file_list, 1):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename + '.encrypted')

            if not os.path.isfile(input_path):
                continue

            print(f"\n[{idx}/{len(file_list)}] {filename}")

            metadata = {
                'original_filename': filename,
                'encrypted_by': 'ImageGhost v3.0'
            }

            if self.encrypt_file(input_path, output_path, password, metadata):
                stats['success'] += 1
            else:
                stats['failed'] += 1

        print("\n" + "=" * 60)
        print(f"\n[+] Encryption Complete!")
        print(f"    Success: {stats['success']}")
        print(f"    Failed: {stats['failed']}")

        return stats

    def generate_secure_password(self, length: int = 32) -> str:
        """
        Generate cryptographically secure random password

        Args:
            length: Password length

        Returns:
            Random password
        """
        import string
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(length))

        if self.verbose:
            print(f"[+] Generated secure password ({length} characters)")

        return password

    def verify_password_strength(self, password: str) -> Tuple[bool, str]:
        """
        Verify password meets security requirements

        Args:
            password: Password to verify

        Returns:
            Tuple of (is_strong, message)
        """
        if len(password) < 12:
            return False, "Password must be at least 12 characters"

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)

        if not (has_upper and has_lower and has_digit and has_special):
            return False, "Password must contain uppercase, lowercase, digit, and special character"

        return True, "Password is strong"

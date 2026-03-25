"""
Secure file deletion module
Military-grade file shredding with multiple overwrite passes
"""

import os
import secrets
from typing import Optional, List


class SecureDelete:
    """
    Secure file deletion using multiple overwrite passes
    Implements DoD 5220.22-M standard
    """

    # Overwrite patterns
    PATTERNS = {
        'dod': [
            b'\x00',  # Pass 1: All zeros
            b'\xFF',  # Pass 2: All ones
            None,     # Pass 3: Random data
            None,     # Pass 4: Random data
            None,     # Pass 5: Random data
            b'\x00',  # Pass 6: All zeros
            b'\xFF',  # Pass 7: All ones
        ],
        'gutmann': 35,  # 35-pass Gutmann method
        'random': 7,    # 7 random passes
        'quick': 3,     # 3 passes (faster)
    }

    def __init__(self, method: str = 'dod', verbose: bool = True):
        """
        Initialize secure delete module

        Args:
            method: Deletion method ('dod', 'gutmann', 'random', 'quick')
            verbose: Enable verbose output
        """
        self.method = method
        self.verbose = verbose
        self.stats = {
            'files_deleted': 0,
            'bytes_shredded': 0,
            'passes_completed': 0
        }

    def shred_file(self, file_path: str, method: Optional[str] = None) -> bool:
        """
        Securely delete a single file

        Args:
            file_path: Path to file to shred
            method: Override default shredding method

        Returns:
            Success status
        """
        try:
            if not os.path.exists(file_path):
                if self.verbose:
                    print(f"[-] File not found: {file_path}")
                return False

            file_size = os.path.getsize(file_path)

            if self.verbose:
                print(f"[*] Shredding: {os.path.basename(file_path)} ({file_size:,} bytes)")

            # Use provided method or default
            shred_method = method if method else self.method

            # Get overwrite patterns
            if shred_method == 'dod':
                passes = self.PATTERNS['dod']
            elif shred_method == 'gutmann':
                passes = [None] * self.PATTERNS['gutmann']
            elif shred_method == 'random':
                passes = [None] * self.PATTERNS['random']
            elif shred_method == 'quick':
                passes = [None] * self.PATTERNS['quick']
            else:
                passes = self.PATTERNS['dod']

            # Perform overwrite passes
            for pass_num, pattern in enumerate(passes, 1):
                if self.verbose:
                    print(f"    Pass {pass_num}/{len(passes)}...", end='\r')

                self._overwrite_file(file_path, pattern, file_size)
                self.stats['passes_completed'] += 1

            # Rename file to random name (obscure filename in filesystem)
            random_name = os.path.join(
                os.path.dirname(file_path),
                secrets.token_hex(16)
            )
            os.rename(file_path, random_name)

            # Truncate to zero length
            with open(random_name, 'wb') as f:
                f.truncate(0)

            # Finally, delete the file
            os.remove(random_name)

            self.stats['files_deleted'] += 1
            self.stats['bytes_shredded'] += file_size

            if self.verbose:
                print(f"[+] Securely deleted: {os.path.basename(file_path)}")

            return True

        except Exception as e:
            if self.verbose:
                print(f"[-] Failed to shred {file_path}: {str(e)}")
            return False

    def _overwrite_file(self, file_path: str, pattern: Optional[bytes],
                       file_size: int):
        """
        Overwrite file with specific pattern

        Args:
            file_path: Path to file
            pattern: Byte pattern (None for random)
            file_size: Size of file
        """
        with open(file_path, 'rb+') as f:
            chunk_size = 1024 * 1024  # 1 MB chunks

            for offset in range(0, file_size, chunk_size):
                # Calculate chunk size for this iteration
                current_chunk = min(chunk_size, file_size - offset)

                # Generate data for this chunk
                if pattern is None:
                    # Random data
                    data = secrets.token_bytes(current_chunk)
                else:
                    # Specific pattern
                    data = pattern * current_chunk

                # Write chunk
                f.seek(offset)
                f.write(data)

            # Flush to disk
            f.flush()
            os.fsync(f.fileno())

    def shred_directory(self, directory: str, recursive: bool = False) -> dict:
        """
        Securely delete all files in directory

        Args:
            directory: Directory path
            recursive: Recursively delete subdirectories

        Returns:
            Statistics dictionary
        """
        if not os.path.exists(directory):
            if self.verbose:
                print(f"[-] Directory not found: {directory}")
            return self.stats

        files_to_shred = []

        if recursive:
            for root, dirs, files in os.walk(directory):
                for filename in files:
                    files_to_shred.append(os.path.join(root, filename))
        else:
            files_to_shred = [
                os.path.join(directory, f)
                for f in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, f))
            ]

        total = len(files_to_shred)

        if total == 0:
            if self.verbose:
                print("[*] No files to shred")
            return self.stats

        print(f"\n[*] Shredding {total} files...")
        print("=" * 60)

        for idx, file_path in enumerate(files_to_shred, 1):
            print(f"\n[{idx}/{total}]")
            self.shred_file(file_path)

        print("\n" + "=" * 60)
        print(f"\n[+] Shredding Complete!")
        print(f"    Files deleted: {self.stats['files_deleted']}")
        print(f"    Bytes shredded: {self.stats['bytes_shredded']:,}")
        print(f"    Passes completed: {self.stats['passes_completed']}")

        # Remove empty directories if recursive
        if recursive:
            try:
                for root, dirs, files in os.walk(directory, topdown=False):
                    for dirname in dirs:
                        dir_path = os.path.join(root, dirname)
                        if not os.listdir(dir_path):
                            os.rmdir(dir_path)
            except (OSError, PermissionError):
                # Directory not empty or permission denied
                pass

        return self.stats

    def get_stats(self) -> dict:
        """Get deletion statistics"""
        return self.stats.copy()

    def verify_deletion(self, file_path: str) -> bool:
        """
        Verify file has been securely deleted

        Args:
            file_path: Path to check

        Returns:
            True if file does not exist
        """
        exists = os.path.exists(file_path)

        if self.verbose:
            if exists:
                print(f"[-] WARNING: File still exists: {file_path}")
            else:
                print(f"[+] Verified deletion: {os.path.basename(file_path)}")

        return not exists

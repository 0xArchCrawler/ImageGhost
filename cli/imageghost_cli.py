#!/usr/bin/env python3
# imageghost cli
# command line interface for batch processing

import sys
import os
import argparse
import getpass
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scrubber import ImageScrubber
from core.crypto import ImageCrypto
from core.secure_delete import SecureDelete


class Colors:
    """ANSI color codes - Arch Linux blue theme"""
    # Arch blue theme colors
    BLUE = '\033[38;5;39m'       # Arch blue (#1793d1)
    CYAN = '\033[38;5;51m'       # Light cyan
    GREEN = '\033[38;5;46m'      # Success green
    YELLOW = '\033[38;5;220m'    # Warning yellow
    RED = '\033[38;5;196m'       # Error red
    PURPLE = '\033[38;5;141m'    # Purple accent
    GRAY = '\033[38;5;240m'      # Dark gray
    WHITE = '\033[38;5;255m'     # Bright white

    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

    @staticmethod
    def info(msg):
        return f"{Colors.BLUE}[*]{Colors.RESET} {msg}"

    @staticmethod
    def success(msg):
        return f"{Colors.GREEN}[+]{Colors.RESET} {msg}"

    @staticmethod
    def error(msg):
        return f"{Colors.RED}[-]{Colors.RESET} {msg}"

    @staticmethod
    def warning(msg):
        return f"{Colors.YELLOW}[!]{Colors.RESET} {msg}"

    @staticmethod
    def header(msg):
        return f"{Colors.BOLD}{Colors.BLUE}{msg}{Colors.RESET}"

    @staticmethod
    def dim(msg):
        return f"{Colors.DIM}{Colors.GRAY}{msg}{Colors.RESET}"


class ImageGhostCLI:
    """command line interface"""

    def __init__(self):
        pass

    def print_banner(self):
        """print colored banner with Arch blue theme"""
        banner = f"""
{Colors.BLUE}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   {Colors.CYAN}██╗███╗   ███╗ █████╗  ██████╗ ███████╗                    {Colors.BLUE}║
║   {Colors.CYAN}██║████╗ ████║██╔══██╗██╔════╝ ██╔════╝                    {Colors.BLUE}║
║   {Colors.CYAN}██║██╔████╔██║███████║██║  ███╗█████╗                      {Colors.BLUE}║
║   {Colors.CYAN}██║██║╚██╔╝██║██╔══██║██║   ██║██╔══╝                      {Colors.BLUE}║
║   {Colors.CYAN}██║██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗                    {Colors.BLUE}║
║   {Colors.CYAN}╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝                    {Colors.BLUE}║
║                                                              ║
║    {Colors.CYAN}██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗              {Colors.BLUE}║
║   {Colors.CYAN}██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝              {Colors.BLUE}║
║   {Colors.CYAN}██║  ███╗███████║██║   ██║███████╗   ██║                 {Colors.BLUE}║
║   {Colors.CYAN}██║   ██║██╔══██║██║   ██║╚════██║   ██║                 {Colors.BLUE}║
║   {Colors.CYAN}╚██████╔╝██║  ██║╚██████╔╝███████║   ██║                 {Colors.BLUE}║
║    {Colors.CYAN}╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝                 {Colors.BLUE}║
║                                                              ║
║   {Colors.WHITE}{Colors.BOLD}Privacy-First Metadata Scrubber{Colors.RESET} {Colors.BLUE}│ {Colors.GRAY}v3.0{Colors.RESET}              {Colors.BLUE}║
║   {Colors.DIM}{Colors.GRAY}Red Team Operations • Zero-Trust Security{Colors.RESET}              {Colors.BLUE}║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
        print(banner)

    def scrub_command(self, args):
        """handle scrub command"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'═' * 65}{Colors.RESET}")
        print(Colors.header("  METADATA SCRUBBING"))
        print(f"{Colors.BOLD}{Colors.BLUE}{'═' * 65}{Colors.RESET}\n")

        scrubber = ImageScrubber(verbose=args.verbose)

        if args.input and os.path.isfile(args.input):
            # single file
            print(Colors.info(f"Processing single file: {Colors.CYAN}{args.input}{Colors.RESET}"))
            output = args.output or args.input.replace('.', '_clean.')
            success, info = scrubber.scrub_image(args.input, output)

            if success:
                print(Colors.success(f"Metadata removed: {Colors.GREEN}{output}{Colors.RESET}"))

                # Display what was exposed before
                self._display_metadata_analysis(info)

                if args.encrypt:
                    self._encrypt_output(output, args)

                if args.shred:
                    self._shred_original(args.input, args)
            else:
                print(Colors.error("Failed to scrub metadata"))

        elif args.input and os.path.isdir(args.input):
            # batch mode
            output_dir = args.output or os.path.join(args.input, '_cleaned')
            print(Colors.info(f"Batch processing directory: {Colors.CYAN}{args.input}{Colors.RESET}"))
            print(Colors.dim(f"Output directory: {output_dir}"))

            results = scrubber.batch_scrub(args.input, output_dir)

            print(Colors.success(f"Processed {Colors.GREEN}{len(results)}{Colors.RESET} images"))

            if args.encrypt:
                self._batch_encrypt(output_dir, args)

            if args.shred:
                self._batch_shred(args.input, args)

        else:
            print(Colors.error(f"Invalid input: {args.input}"))

    def encrypt_command(self, args):
        """handle encrypt command"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'═' * 65}{Colors.RESET}")
        print(Colors.header("  FILE ENCRYPTION"))
        print(f"{Colors.BOLD}{Colors.BLUE}{'═' * 65}{Colors.RESET}\n")

        crypto = ImageCrypto(verbose=args.verbose)
        password = self._get_password(args)

        if os.path.isfile(args.input):
            print(Colors.info(f"Encrypting file: {Colors.CYAN}{args.input}{Colors.RESET}"))
            output = args.output or (args.input + '.encrypted')
            crypto.encrypt_file(args.input, output, password)
            print(Colors.success(f"Encrypted: {Colors.GREEN}{output}{Colors.RESET}"))

            if args.shred:
                self._shred_original(args.input, args)

        elif os.path.isdir(args.input):
            print(Colors.info(f"Batch encrypting directory: {Colors.CYAN}{args.input}{Colors.RESET}"))
            output_dir = args.output or os.path.join(args.input, '_encrypted')
            print(Colors.dim(f"Output directory: {output_dir}"))
            crypto.batch_encrypt(args.input, output_dir, password)
            print(Colors.success("Encryption complete"))

            if args.shred:
                self._batch_shred(args.input, args)

    def decrypt_command(self, args):
        """handle decrypt command"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'═' * 65}{Colors.RESET}")
        print(Colors.header("  FILE DECRYPTION"))
        print(f"{Colors.BOLD}{Colors.BLUE}{'═' * 65}{Colors.RESET}\n")

        crypto = ImageCrypto(verbose=args.verbose)
        password = getpass.getpass(f"{Colors.BLUE}[*]{Colors.RESET} Enter decryption password: ")

        if os.path.isfile(args.input):
            print(Colors.info(f"Decrypting file: {Colors.CYAN}{args.input}{Colors.RESET}"))
            output = args.output or args.input.replace('.encrypted', '')
            success, metadata = crypto.decrypt_file(args.input, output, password)

            if success:
                print(Colors.success(f"Decrypted: {Colors.GREEN}{output}{Colors.RESET}"))

                if metadata:
                    print(f"\n{Colors.BOLD}{Colors.BLUE}Embedded Metadata:{Colors.RESET}")
                    for key, value in metadata.items():
                        print(f"  {Colors.CYAN}{key}{Colors.RESET}: {value}")
            else:
                print(Colors.error("Decryption failed - incorrect password or corrupted file"))

    def pipeline_command(self, args):
        """full pipeline: scrub -> encrypt -> shred"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'═' * 65}{Colors.RESET}")
        print(Colors.header("  FULL PIPELINE MODE"))
        print(f"{Colors.BOLD}{Colors.BLUE}{'═' * 65}{Colors.RESET}")
        print(f"{Colors.DIM}{Colors.GRAY}  Scrub → Encrypt → Secure Delete{Colors.RESET}\n")

        if not os.path.isdir(args.input):
            print(Colors.error("Pipeline requires input directory"))
            return

        # step 1: scrub
        print(f"\n{Colors.BOLD}{Colors.CYAN}[1/3]{Colors.RESET} {Colors.info('Scrubbing metadata...')}")
        scrubber = ImageScrubber(verbose=args.verbose)
        temp_dir = os.path.join(args.input, '_temp_scrubbed')
        results = scrubber.batch_scrub(args.input, temp_dir)
        print(Colors.success(f"Scrubbed {len(results)} images"))

        # step 2: encrypt
        print(f"\n{Colors.BOLD}{Colors.CYAN}[2/3]{Colors.RESET} {Colors.info('Encrypting files...')}")
        crypto = ImageCrypto(verbose=args.verbose)
        password = self._get_password(args)
        output_dir = args.output or os.path.join(args.input, '_final_encrypted')
        crypto.batch_encrypt(temp_dir, output_dir, password)
        print(Colors.success("Encryption complete"))

        # step 3: shred
        print(f"\n{Colors.BOLD}{Colors.CYAN}[3/3]{Colors.RESET} {Colors.info('Securely deleting temporary files...')}")
        deleter = SecureDelete(method=args.shred_method, verbose=args.verbose)
        deleter.shred_directory(temp_dir, recursive=True)
        print(Colors.success("Temporary files shredded"))

        try:
            os.rmdir(temp_dir)
        except:
            pass

        if args.shred_originals:
            print(f"\n{Colors.WARNING}{Colors.YELLOW}[!]{Colors.RESET} {Colors.warning('Shredding original files...')}")
            deleter.shred_directory(args.input, recursive=False)
            print(Colors.success("Original files shredded"))

        print(f"\n{Colors.BOLD}{Colors.BLUE}{'═' * 65}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}[✓] PIPELINE COMPLETE!{Colors.RESET}")
        print(f"{Colors.BLUE}[*]{Colors.RESET} Encrypted files: {Colors.CYAN}{output_dir}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'═' * 65}{Colors.RESET}\n")

    def _get_password(self, args):
        """get password"""
        if args.password:
            return args.password

        password = getpass.getpass(f"{Colors.BLUE}[*]{Colors.RESET} Enter encryption password: ")
        confirm = getpass.getpass(f"{Colors.BLUE}[*]{Colors.RESET} Confirm password: ")

        if password != confirm:
            print(Colors.error("Passwords don't match"))
            sys.exit(1)

        crypto = ImageCrypto()
        is_strong, msg = crypto.verify_password_strength(password)

        if not is_strong:
            print(Colors.warning(f"Weak password: {msg}"))
            use_anyway = input(f"{Colors.YELLOW}[?]{Colors.RESET} Use anyway? (y/N): ")
            if use_anyway.lower() != 'y':
                sys.exit(1)
        else:
            print(Colors.success("Strong password accepted"))

        return password

    def _encrypt_output(self, output_path, args):
        """encrypt output file"""
        crypto = ImageCrypto(verbose=args.verbose)
        password = self._get_password(args)

        encrypted_path = output_path + '.encrypted'
        crypto.encrypt_file(output_path, encrypted_path, password)

        if args.shred:
            deleter = SecureDelete(method=args.shred_method, verbose=False)
            deleter.shred_file(output_path)
        else:
            os.remove(output_path)

    def _batch_encrypt(self, directory, args):
        """batch encrypt"""
        crypto = ImageCrypto(verbose=args.verbose)
        password = self._get_password(args)

        encrypted_dir = directory + '_encrypted'
        crypto.batch_encrypt(directory, encrypted_dir, password)

        if args.shred:
            deleter = SecureDelete(method=args.shred_method, verbose=False)
            deleter.shred_directory(directory, recursive=False)

    def _shred_original(self, file_path, args):
        """shred original"""
        deleter = SecureDelete(method=args.shred_method, verbose=args.verbose)
        deleter.shred_file(file_path)

    def _batch_shred(self, directory, args):
        """batch shred"""
        deleter = SecureDelete(method=args.shred_method, verbose=args.verbose)
        deleter.shred_directory(directory, recursive=False)

    def _display_metadata_analysis(self, info):
        """display metadata exposure analysis"""
        original_metadata = info.get('original_metadata', {})
        bytes_removed = info.get('bytes_removed', 0)

        if not original_metadata:
            print(f"\n{Colors.dim('No metadata detected in original image')}")
            return

        print(f"\n{Colors.BOLD}{Colors.YELLOW}{'─' * 65}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.RED}  METADATA EXPOSURE ANALYSIS{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}{'─' * 65}{Colors.RESET}\n")

        # Count sensitive fields
        sensitive_fields = {
            'GPS': ['GPS', 'GPSLatitude', 'GPSLongitude', 'GPSAltitude'],
            'Camera': ['Make', 'Model', 'LensModel', 'SerialNumber'],
            'Location': ['Location', 'City', 'State', 'Country'],
            'Software': ['Software', 'ProcessingSoftware', 'CreatorTool'],
            'Personal': ['Artist', 'Copyright', 'Owner', 'Author'],
            'Timestamps': ['CreateDate', 'ModifyDate', 'DateTimeOriginal']
        }

        exposed_categories = {}
        for category, keywords in sensitive_fields.items():
            found = []
            for key, value in original_metadata.items():
                if any(kw.lower() in key.lower() for kw in keywords):
                    found.append(f"{key}: {value}")
            if found:
                exposed_categories[category] = found

        # Display exposed data by category
        if exposed_categories:
            print(f"{Colors.RED}[!]{Colors.RESET} {Colors.BOLD}The following sensitive data was EXPOSED:{Colors.RESET}\n")

            for category, items in exposed_categories.items():
                icon = "📍" if category == "GPS" else "📷" if category == "Camera" else "🏙️" if category == "Location" else "💻" if category == "Software" else "👤" if category == "Personal" else "🕐"
                print(f"  {icon} {Colors.BOLD}{Colors.RED}{category}:{Colors.RESET}")
                for item in items[:3]:  # Show max 3 items per category
                    print(f"    {Colors.DIM}{Colors.GRAY}• {item}{Colors.RESET}")
                if len(items) > 3:
                    print(f"    {Colors.DIM}{Colors.GRAY}• ... and {len(items) - 3} more{Colors.RESET}")
                print()

        # Display bytes removed
        print(f"{Colors.GREEN}[✓]{Colors.RESET} {Colors.BOLD}Metadata Removed:{Colors.RESET} {Colors.GREEN}{bytes_removed:,} bytes{Colors.RESET}")

        # Display after state
        print(f"\n{Colors.BOLD}{Colors.GREEN}{'─' * 65}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}  ✓ IMAGE NOW CLEAN{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}{'─' * 65}{Colors.RESET}")
        print(f"{Colors.dim('All metadata removed • No traces left • Safe to share')}\n")


def main():
    cli = ImageGhostCLI()
    cli.print_banner()

    parser = argparse.ArgumentParser(
        description='imageghost - multi-image fingerprint scrubber',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='commands')

    # scrub
    scrub_parser = subparsers.add_parser('scrub', help='scrub metadata')
    scrub_parser.add_argument('input', help='input file or directory')
    scrub_parser.add_argument('-o', '--output', help='output file or directory')
    scrub_parser.add_argument('-e', '--encrypt', action='store_true', help='encrypt after scrubbing')
    scrub_parser.add_argument('-s', '--shred', action='store_true', help='securely delete originals')
    scrub_parser.add_argument('--shred-method', default='dod', choices=['dod', 'gutmann', 'random', 'quick'])
    scrub_parser.add_argument('-v', '--verbose', action='store_true', default=True)
    scrub_parser.add_argument('-p', '--password', help='encryption password')

    # encrypt
    encrypt_parser = subparsers.add_parser('encrypt', help='encrypt files')
    encrypt_parser.add_argument('input', help='input file or directory')
    encrypt_parser.add_argument('-o', '--output', help='output file or directory')
    encrypt_parser.add_argument('-s', '--shred', action='store_true', help='securely delete originals')
    encrypt_parser.add_argument('--shred-method', default='dod', choices=['dod', 'gutmann', 'random', 'quick'])
    encrypt_parser.add_argument('-v', '--verbose', action='store_true', default=True)
    encrypt_parser.add_argument('-p', '--password', help='encryption password')

    # decrypt
    decrypt_parser = subparsers.add_parser('decrypt', help='decrypt files')
    decrypt_parser.add_argument('input', help='input file')
    decrypt_parser.add_argument('-o', '--output', help='output file')
    decrypt_parser.add_argument('-v', '--verbose', action='store_true', default=True)

    # pipeline
    pipeline_parser = subparsers.add_parser('pipeline', help='full pipeline')
    pipeline_parser.add_argument('input', help='input directory')
    pipeline_parser.add_argument('-o', '--output', help='output directory')
    pipeline_parser.add_argument('--shred-originals', action='store_true')
    pipeline_parser.add_argument('--shred-method', default='dod', choices=['dod', 'gutmann', 'random', 'quick'])
    pipeline_parser.add_argument('-v', '--verbose', action='store_true', default=True)
    pipeline_parser.add_argument('-p', '--password', help='encryption password')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'scrub':
        cli.scrub_command(args)
    elif args.command == 'encrypt':
        cli.encrypt_command(args)
    elif args.command == 'decrypt':
        cli.decrypt_command(args)
    elif args.command == 'pipeline':
        cli.pipeline_command(args)


if __name__ == '__main__':
    main()

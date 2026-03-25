#!/usr/bin/env python3
# imageghost - main entry point

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == 'cli':
        sys.argv.pop(1)
        from cli.imageghost_cli import main as cli_main
        cli_main()

    elif mode in ['gui', 'web']:
        from web.app import run_server
        host = '127.0.0.1'
        port = 5000
        debug = False

        # parse optional arguments
        for i, arg in enumerate(sys.argv[2:], start=2):
            if arg == '--host' and i + 1 < len(sys.argv):
                host = sys.argv[i + 1]
            elif arg == '--port' and i + 1 < len(sys.argv):
                port = int(sys.argv[i + 1])
            elif arg == '--debug':
                debug = True

        dashboard_type = "web dashboard" if mode == 'web' else "gui (web interface)"
        print(f"[*] starting imageghost v3.0 {dashboard_type}")
        print(f"[*] server: http://{host}:{port}")
        print(f"[*] open your browser and navigate to the URL above")
        print(f"[*] press ctrl+c to stop\n")
        run_server(host=host, port=port, debug=debug)

    elif mode in ['-h', '--help', 'help']:
        print_usage()

    else:
        print(f"unknown mode: {mode}")
        print_usage()
        sys.exit(1)


def print_usage():
    print("""
╔══════════════════════════════════════════════════════╗
║                  IMAGEGHOST v3.0                     ║
║           multi-image fingerprint scrubber           ║
╚══════════════════════════════════════════════════════╝

usage:
    python3 imageghost.py cli <command> [options]
    python3 imageghost.py gui [--host HOST] [--port PORT] [--debug]
    python3 imageghost.py web [--host HOST] [--port PORT] [--debug]

modes:
    cli         command-line interface
    gui         web dashboard interface (same as web)
    web         web dashboard interface (browser-based)

examples:
    # scrub metadata from images (cli)
    python3 imageghost.py cli scrub /path/to/images -o /path/to/output

    # full pipeline (cli)
    python3 imageghost.py cli pipeline /path/to/images --shred-originals

    # launch web dashboard
    python3 imageghost.py gui
    python3 imageghost.py web
    python3 imageghost.py web --port 8080
    python3 imageghost.py web --host 0.0.0.0 --port 8080

help:
    python3 imageghost.py cli --help
    """)


if __name__ == '__main__':
    main()

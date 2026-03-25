<div align="center">

# 👻 ImageGhost

**Professional Multi-Image Fingerprint Scrubber for Red Teams & Penetration Testers**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)](https://www.linux.org/)
[![Version](https://img.shields.io/badge/version-3.0-green.svg)](VERSION)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

*Operational security through complete metadata elimination, military-grade encryption, and secure file destruction*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
  - [CLI Mode](#cli-mode)
  - [Web Dashboard (GUI Mode)](#web-dashboard-gui-mode)
- [Supported Formats](#-supported-formats)
- [Security](#-security)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)
- [Disclaimer](#%EF%B8%8F-disclaimer)

---

## 🎯 Overview

**ImageGhost** is a professional-grade metadata scrubbing and encryption tool designed for privacy-conscious individuals, red team operators, security professionals, and zero-trust advocates. It provides complete operational security by eliminating ALL traces of metadata from images, encrypting them with military-grade encryption, and securely deleting originals.

**Perfect for:**
- Privacy-concerned individuals protecting personal data
- Red team operations and penetration testing
- Offensive security professionals
- Zero-trust security practitioners
- Security researchers and professionals
- Journalists safeguarding source privacy
- Human rights defenders
- CTF competitions and security challenges
- Anyone valuing digital privacy and OPSEC

### Why ImageGhost?

- **Complete Metadata Removal**: EXIF, GPS, XMP, IPTC, thumbnails, ICC profiles, embedded images
- **Steganography Detection**: Identifies and removes potential hidden data using LSB normalization
- **Military-Grade Encryption**: AES-256-GCM with Argon2id key derivation
- **Secure Deletion**: DoD 5220.22-M and Gutmann 35-pass file shredding
- **Batch Processing**: Handle 50-100+ images simultaneously with parallel processing
- **Two Interfaces**: CLI with Arch Linux blue theme and Web Dashboard with 9 professional themes
- **Metadata Exposure Analysis**: See what was exposed before scrubbing (GPS, Camera, Timestamps)
- **46+ Format Support**: JPEG, PNG, RAW, PSD, TIFF, WebP, and more

---

## ✨ Features

### 🧹 Metadata Scrubbing

<details>
<summary><b>4-Layer Cleaning Process</b></summary>

1. **PIL Complete Rewrite** - Removes basic EXIF, thumbnails, and embedded data
2. **ExifTool Nuclear Option** - Eliminates ALL metadata tags (XMP, IPTC, Adobe, ICC profiles)
3. **Steganography Stripping** - Normalizes LSB bits to remove hidden data
4. **Re-encoding** - Ensures absolute clean state

</details>

**Removes:**
- ✅ EXIF data (camera model, settings, lens information)
- ✅ GPS coordinates (latitude, longitude, altitude, timestamps)
- ✅ Timestamps (created, modified, digitized)
- ✅ XMP tags (Adobe Lightroom, Photoshop metadata)
- ✅ IPTC tags (copyright, keywords, author)
- ✅ Thumbnails & preview images
- ✅ ICC color profiles & color space data
- ✅ Software signatures & tool watermarks
- ✅ Comments, descriptions, and keywords
- ✅ Steganography traces (LSB normalization)

### 🔐 Encryption

**Algorithm**: AES-256-GCM (Authenticated Encryption with Associated Data)
**Key Derivation**: Argon2id with hardened parameters
- Time cost: 4 iterations
- Memory: 64 MB
- Parallelism: 4 threads
- Salt: 256-bit cryptographically secure random

**Features:**
- End-to-end encryption
- Authenticated encryption prevents tampering
- Password strength validation
- Secure password generator
- Metadata embedding in encrypted container

### 🗑️ Secure Deletion

**Methods:**
- **DoD 5220.22-M**: 7-pass overwrite (Default)
- **Gutmann Method**: 35-pass overwrite (Maximum security)
- **Random 7-Pass**: 7 random data passes
- **Quick 3-Pass**: Fast secure deletion

**Process:**
1. Multiple overwrite passes with patterns
2. Filename obfuscation (random rename)
3. File truncation to zero length
4. Final deletion with verification

### 🎨 User Interfaces

#### CLI (Command Line)
- **Professional Arch Linux Blue Theme**: Colored output with ANSI codes
- **Metadata Exposure Analysis**: Shows what was exposed before/after scrubbing
  - GPS coordinates, Camera info, Timestamps
  - Personal data, Software signatures
  - Categorized display with icons
- **Batch Processing**: Handle 50+ images with progress tracking
- **Pipeline Mode**: Full workflow (scrub → encrypt → shred)
- **Direct File/Folder Operations**: Single file or entire directories
- **Password Strength Validation**: Ensures secure encryption keys

#### Web Dashboard (Browser-based GUI)
- **9 Professional Themes**:
  1. Arch Blue (Default) - Clean minimal design
  2. BlackArch - Green terminal style
  3. Dracula - Purple/pink aesthetic
  4. Gruvbox - Warm retro colors
  5. Green Hacker - Matrix-style theme
  6. Blue SOC Team - Professional blue
  7. Red Team Ops - Aggressive red
  8. Purple Team - Combined operations
  9. Nord - Arctic blue/white
- **Modern Interface**: Sidebar navigation with SVG icons
- **Drag & Drop**: Multi-file upload (50-100+ images)
- **WebSocket Real-time**: Live progress updates
- **Job Management**: Track multiple operations
- **Secure Password Generator**: Cryptographically secure
- **Theme Persistence**: Saves selected theme

---

## 📦 Installation

### Prerequisites

- **OS**: Linux (Arch, Kali, Ubuntu, Debian, etc.)
- **Python**: 3.7 or higher
- **pip**: Python package manager

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/ImageGhost.git
cd ImageGhost

# Install Python dependencies
pip3 install -r requirements.txt

# Make scripts executable
chmod +x imageghost.py
chmod +x cli/imageghost_cli.py

# Optional: Install system tools for enhanced features
sudo apt install exiftool dcraw  # Debian/Ubuntu/Kali
sudo pacman -S perl-image-exiftool dcraw  # Arch Linux
```

### Dependencies

**Core:**
- `Pillow >= 10.0.0` - Image processing
- `cryptography >= 41.0.0` - Encryption
- `argon2-cffi >= 23.1.0` - Key derivation
- `pycryptodome >= 3.19.0` - Cryptographic primitives

**Web Dashboard:**
- `Flask >= 3.0.0` - Web framework
- `flask-socketio >= 5.3.0` - Real-time communication
- `python-socketio >= 5.10.0` - WebSocket support
- `eventlet >= 0.33.0` - Async server support

**Optional:**
- `exiftool` - Enhanced metadata removal
- `dcraw` - RAW camera format support

---

## 🚀 Quick Start

### 30-Second Tutorial

```bash
# Scrub metadata from a single image
python3 imageghost.py cli scrub image.jpg -o clean_image.jpg

# Batch scrub a folder
python3 imageghost.py cli scrub /path/to/images -o /path/to/output

# Full pipeline (scrub → encrypt → shred originals)
python3 imageghost.py cli pipeline /path/to/images -p MySecurePassword123!

# Launch web dashboard (GUI)
python3 imageghost.py gui
# or
python3 imageghost.py web
```

---

## 📖 Usage

### CLI Mode

#### Scrub Metadata

```bash
# Basic scrubbing
python3 imageghost.py cli scrub input_folder -o output_folder

# Scrub with encryption
python3 imageghost.py cli scrub input_folder -e -p "SecurePass123!"

# Scrub + encrypt + shred originals
python3 imageghost.py cli scrub input_folder -e -s --shred-method dod
```

#### Encrypt Files

```bash
# Encrypt cleaned images
python3 imageghost.py cli encrypt input_folder -p "MyPassword"

# Decrypt files
python3 imageghost.py cli decrypt encrypted_file.enc -o decrypted_image.jpg
```

#### Full Pipeline

```bash
# Complete workflow: scrub → encrypt → shred
python3 imageghost.py cli pipeline /sensitive/images \\
    --shred-originals \\
    --shred-method gutmann \\
    -p "Ultra-Secure-Password-2024!"
```

### Web Dashboard (GUI Mode)

```bash
# Start web dashboard (localhost:5000)
python3 imageghost.py gui
# or
python3 imageghost.py web

# Custom port
python3 imageghost.py gui --port 8080

# Network accessible (bind to all interfaces)
python3 imageghost.py gui --host 0.0.0.0 --port 8080

# Debug mode
python3 imageghost.py gui --debug
```

Access via browser: `http://localhost:5000`

**Note:** Both `gui` and `web` commands launch the same web dashboard interface.

**Features:**
- **Modern Browser Interface**: Premium sidebar navigation with SVG icons
- **Drag & Drop Upload**: Handle 50-100+ images simultaneously
- **Real-time Updates**: WebSocket-powered live progress tracking
- **Multiple Jobs**: Run scrub, encrypt, decrypt operations concurrently
- **Live Console**: Real-time logging of all operations
- **Job History**: Track and manage all processing tasks
- **9 Professional Themes**:
  1. **Arch Blue** (Default) - Clean minimal with Arch Linux #1793d1 accent
  2. **BlackArch** - Green terminal hacker style
  3. **Dracula** - Purple/pink aesthetic
  4. **Gruvbox** - Warm retro colors
  5. **Green Hacker** - Matrix-style green
  6. **Blue SOC Team** - Professional blue tones
  7. **Red Team Ops** - Aggressive red theme
  8. **Purple Team** - Combined operations purple
  9. **Nord** - Arctic blue/white minimalist
- **Secure Password Generator**: Cryptographically secure random passwords
- **Settings Configuration**: Customize scrubbing and encryption options
- **Batch Operations**: Process multiple files simultaneously

---

## 🖼️ Supported Formats

**46+ Image Formats**

| Category | Formats |
|----------|---------|
| **Standard Raster** | JPG, JPEG, PNG, GIF, BMP, TIFF, WebP, ICO, SVG |
| **RAW Camera** | CR2 (Canon), NEF (Nikon), ARW (Sony), DNG (Adobe), ORF (Olympus), RW2 (Panasonic), PEF (Pentax), SRW (Samsung), RAF (Fujifilm) |
| **Professional** | PSD, PSB (Photoshop), XCF (GIMP), KRA (Krita) |
| **Legacy** | PCX, TGA, ICNS, JP2, J2K, JPF, JPX |
| **HDR** | HDR, EXR, PFM |
| **Medical** | DCM, DICOM |
| **Misc** | PPM, PGM, PBM, PNM, XBM, XPM |

---

## 🔒 Security

### Threat Model

ImageGhost protects against:
- ✅ Metadata-based attribution & tracking
- ✅ GPS location disclosure
- ✅ Camera & device fingerprinting
- ✅ Timestamp correlation
- ✅ Software watermarking
- ✅ Steganographic data hiding
- ✅ Forensic recovery of originals

### Security Features

1. **No External Connections** - All processing is local
2. **Secure Random Generation** - Cryptographically secure `secrets` module
3. **Memory Clearing** - Sensitive data cleared after use
4. **Verified Deletion** - Multiple overwrite passes prevent recovery
5. **Authenticated Encryption** - AEAD prevents tampering
6. **Strong KDF** - Argon2id with hardened parameters
7. **Open Source** - Full code transparency

### Best Practices

```bash
# Maximum security pipeline
python3 imageghost.py cli pipeline /sensitive/images \\
    --shred-method gutmann \\
    --shred-originals \\
    -p "$(openssl rand -base64 32)"

# Verify deletion
ls /sensitive/images  # Should be empty or gone
```

---

## 📚 Documentation

- [QUICKSTART.md](QUICKSTART.md) - 5-minute getting started guide
- [FEATURES.md](FEATURES.md) - Detailed feature documentation
- [THEMES.md](THEMES.md) - GUI theme customization
- [INSTALL.md](INSTALL.md) - Comprehensive installation guide
- [SECURITY.md](SECURITY.md) - Security policy & reporting
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code of Conduct
- Development setup
- Coding standards
- Pull request process
- Issue reporting

### Development

```bash
# Clone repository
git clone https://github.com/yourusername/imageghost.git
cd imageghost

# Install dev dependencies
pip3 install -r requirements.txt
pip3 install pytest black flake8

# Run tests
./run_tests.sh

# Code formatting
black .
flake8 .
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

**FOR PRIVACY PROTECTION AND AUTHORIZED USE**

ImageGhost is designed for:
- ✅ Personal privacy protection
- ✅ Metadata sanitization for public sharing
- ✅ Zero-trust security practices
- ✅ Authorized security testing and research
- ✅ Journalist source protection
- ✅ Human rights documentation
- ✅ Operational security (OPSEC)
- ✅ CTF competitions

**Your Privacy, Your Control.**

Users are responsible for complying with all applicable laws and regulations. This tool is provided for legitimate privacy protection and security purposes. The authors assume no liability for misuse of this tool.

---

## 🌟 Star History

If you find ImageGhost useful, please consider giving it a star! ⭐

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/imageghost/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/imageghost/discussions)
- **Security**: See [SECURITY.md](SECURITY.md) for vulnerability reporting

---

<div align="center">

**Made with 💀 for Red Teams & Security Professionals**

*ImageGhost v3.0 - Professional Metadata Scrubbing & Encryption*

[⬆ Back to Top](#-imageghost)

</div>

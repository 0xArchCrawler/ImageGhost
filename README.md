### Professional Multi-Image Fingerprint Scrubber for Red Teams & Penetration Testers

[![Build Status](https://github.com/0xArchCrawler/ImageGhost/workflows/Tests/badge.svg)](https://github.com/0xArchCrawler/ImageGhost/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)](https://www.linux.org/)
[![Version](https://img.shields.io/badge/version-3.0.0-green.svg)](VERSION)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security](https://img.shields.io/badge/security-AES--256--GCM-brightgreen.svg)](#security)
[![OPSEC](https://img.shields.io/badge/OPSEC-compliant-success.svg)](#security)
[![Stars](https://img.shields.io/github/stars/0xArchCrawler/ImageGhost?style=social)](https://github.com/0xArchCrawler/ImageGhost/stargazers)
[![Forks](https://img.shields.io/github/forks/0xArchCrawler/ImageGhost?style=social)](https://github.com/0xArchCrawler/ImageGhost/network/members)

*Operational security through complete metadata elimination, military-grade encryption, and secure file destruction*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Contributing](#-contributing)

---

### 🚀 Quick Demo

```bash
# One command to scrub, encrypt, and shred originals
python3 imageghost.py cli pipeline /photos -p MySecurePass123!
```

**Result:** Clean images with ZERO metadata, encrypted with AES-256-GCM, originals securely deleted (7-pass DoD)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Why ImageGhost?](#-why-imageghost)
- [Key Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
  - [CLI Mode](#cli-mode)
  - [Web Dashboard](#web-dashboard-gui-mode)
- [Supported Formats](#-supported-formats)
- [Security](#-security)
- [Performance](#-performance)
- [Documentation](#-documentation)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [License](#-license)
- [Disclaimer](#%EF%B8%8F-disclaimer)

---

## 🎯 Overview

**ImageGhost** is a professional-grade metadata scrubbing and encryption tool designed for privacy-conscious individuals, red team operators, security professionals, and zero-trust advocates. It provides complete operational security by eliminating **ALL traces of metadata** from images, encrypting them with military-grade encryption, and securely deleting originals.

### Perfect For:

<table>
<tr>
<td width="50%">

**Privacy & Security:**
- 🔐 Privacy-conscious individuals
- 🛡️ Zero-trust security practitioners
- 📰 Journalists protecting sources
- ✊ Human rights defenders
- 🔍 Security researchers

</td>
<td width="50%">

**Red Team & Offensive:**
- 🎯 Red team operations
- 🔴 Penetration testing
- ⚔️ Offensive security ops
- 🏆 CTF competitions
- 🚀 OPSEC compliance

</td>
</tr>
</table>

---

## 💡 Why ImageGhost?

| Feature | Description | Benefit |
|---------|-------------|---------|
| **🧹 4-Layer Cleaning** | PIL + ExifTool + Stego stripping + Re-encoding | **Complete** metadata removal |
| **🔐 AES-256-GCM** | Military-grade encryption with Argon2id KDF | **Unbreakable** protection |
| **🗑️ DoD Deletion** | 7-pass (DoD) or 35-pass (Gutmann) shredding | **Forensically** secure |
| **⚡ Batch Processing** | 50-100+ images in parallel | **Fast** & efficient |
| **🎨 Dual Interface** | CLI (Arch blue) + Web (9 themes) | **Flexible** usage |
| **📦 46+ Formats** | JPEG, PNG, RAW, PSD, TIFF, WebP, etc. | **Universal** support |
| **🔍 Exposure Analysis** | Before/after metadata comparison | **Visibility** into risks |
| **🌐 Zero External** | 100% local processing | **Complete** privacy |

---

## ✨ Features

### 🧹 Metadata Scrubbing

<details>
<summary><b>4-Layer Cleaning Process (Click to expand)</b></summary>

1. **Layer 1: PIL Complete Rewrite**
   - Removes basic EXIF, thumbnails, and embedded data
   - Strips image comments and descriptions
   - Cleans color profiles

2. **Layer 2: ExifTool Nuclear Option**
   - Eliminates ALL metadata tags
   - Removes XMP, IPTC, Adobe metadata
   - Cleans ICC profiles and color spaces
   - Strips maker notes and proprietary tags

3. **Layer 3: Steganography Stripping**
   - Normalizes LSB (Least Significant Bits)
   - Removes potential hidden data
   - Cleans steganographic traces

4. **Layer 4: Re-encoding**
   - Complete image reconstruction
   - Ensures absolute clean state
   - Verifies no metadata remnants

</details>

**What Gets Removed:**

| Category | Items |
|----------|-------|
| **Location Data** | GPS coordinates, latitude, longitude, altitude, GPS timestamps |
| **Camera Info** | Make, model, lens, settings, serial numbers, firmware |
| **Timestamps** | Creation date, modification date, digitized date, timezone |
| **Software** | Creator software, editing tools, processing history |
| **Personal** | Copyright, author, keywords, descriptions, comments |
| **Technical** | ICC profiles, color spaces, thumbnails, preview images |
| **Hidden** | Steganography traces, LSB data, embedded files |

### 🔐 Encryption

**Algorithm:** AES-256-GCM (Authenticated Encryption with Associated Data)

**Key Derivation:** Argon2id with production-hardened parameters
- **Time cost:** 4 iterations (resistance to time-memory trade-offs)
- **Memory cost:** 64 MB (prevents GPU attacks)
- **Parallelism:** 4 threads (optimized for multi-core)
- **Salt:** 256-bit cryptographically secure random

**Security Features:**
- ✅ End-to-end encryption
- ✅ Authenticated encryption prevents tampering (AEAD)
- ✅ Password strength validation (entropy checking)
- ✅ Secure password generator (96+ bits entropy)
- ✅ Metadata embedding in encrypted container
- ✅ No key material in memory after operations

### 🗑️ Secure Deletion

**Available Methods:**

| Method | Passes | Security Level | Speed | Use Case |
|--------|--------|---------------|-------|----------|
| **Quick 3-Pass** | 3 | Good | ⚡⚡⚡ | Testing, non-critical |
| **DoD 5220.22-M** | 7 | High | ⚡⚡ | Default, standard ops |
| **Gutmann** | 35 | Maximum | ⚡ | Maximum paranoia |
| **Random 7-Pass** | 7 | High | ⚡⚡ | Randomized patterns |

**Deletion Process:**
1. **Overwrite Passes** - Multiple passes with specific patterns
2. **Filename Obfuscation** - Random rename before deletion
3. **File Truncation** - Zero-length file
4. **Final Deletion** - Unlink with verification
5. **Verification** - Confirms complete removal

### 🎨 User Interfaces

#### CLI (Command Line Interface)

**Professional Arch Linux Blue Theme (#1793d1)**

Features:
- 🎨 ANSI colored output (blue, green, red, yellow, gray)
- 📊 Metadata exposure analysis (before/after)
- 📈 Progress tracking with percentage
- ⚡ Batch processing with parallel execution
- 🔄 Pipeline mode (scrub → encrypt → shred)
- 🔐 Password strength validation
- 📁 Direct file/folder operations

**Example Output:**
```
┌─────────────────────────────────────────────┐
│  METADATA EXPOSURE ANALYSIS                 │
├─────────────────────────────────────────────┤
│  📍 GPS: 37.7749° N, 122.4194° W           │
│  📷 Camera: Canon EOS 5D Mark IV            │
│  🕐 Timestamp: 2024-03-15 14:32:18         │
│  ⚠️  HIGH EXPOSURE RISK                     │
└─────────────────────────────────────────────┘
```

#### Web Dashboard (Browser-based GUI)

**9 Professional Themes:**

| Theme | Style | Target Audience | Color Scheme |
|-------|-------|----------------|--------------|
| **Arch Blue** | Clean minimal | General users | #1793d1 blue |
| **BlackArch** | Terminal hacker | Security pros | Green terminal |
| **Dracula** | Modern dark | Developers | Purple/pink |
| **Gruvbox** | Retro warm | Designers | Warm retro |
| **Green Hacker** | Matrix-style | Red teamers | Matrix green |
| **Blue SOC** | Professional | SOC analysts | Professional blue |
| **Red Team** | Aggressive | Red teams | Aggressive red |
| **Purple Team** | Combined ops | Purple teams | Purple tones |
| **Nord** | Arctic minimal | Minimalists | Arctic blue/white |

**Dashboard Features:**
- 🎯 **Modern Sidebar** - Premium navigation with SVG icons
- 📤 **Drag & Drop** - Multi-file upload (50-100+ images)
- 📡 **WebSocket Live** - Real-time progress updates
- 📊 **Job Management** - Track multiple operations
- 🔐 **Password Generator** - Cryptographically secure (96+ bits)
- 🎨 **Theme Switching** - 9 themes with persistence
- 📝 **Live Console** - Real-time operation logging
- 📁 **File Grid** - Visual file display with metadata
- ⚙️ **Settings Panel** - Customize scrubbing options

---

## 📦 Installation

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| **OS** | Linux | Arch, Kali, Ubuntu, Debian, etc. |
| **Python** | 3.7+ | Tested on 3.7-3.11 |
| **pip** | Latest | Python package manager |
| **exiftool** | Optional | Enhanced metadata removal |
| **dcraw** | Optional | RAW camera format support |

### Quick Install (3 commands)

```bash
# 1. Clone repository
git clone https://github.com/0xArchCrawler/ImageGhost.git
cd ImageGhost

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Make executable
chmod +x imageghost.py

# Done! Test it:
python3 imageghost.py --help
```

### System Tools (Optional but Recommended)

```bash
# Debian/Ubuntu/Kali
sudo apt update
sudo apt install exiftool dcraw -y

# Arch Linux
sudo pacman -S perl-image-exiftool dcraw

# Fedora/RHEL
sudo dnf install perl-Image-ExifTool dcraw
```

### Dependencies

<details>
<summary><b>Click to view all dependencies</b></summary>

**Core Python Packages:**
```
Pillow >= 10.0.0          # Image processing
cryptography >= 41.0.0     # Encryption
argon2-cffi >= 23.1.0      # Key derivation
pycryptodome >= 3.19.0     # Crypto primitives
```

**Web Dashboard:**
```
Flask >= 3.0.0             # Web framework
flask-socketio >= 5.3.0    # Real-time comms
python-socketio >= 5.10.0  # WebSocket support
eventlet >= 0.33.0         # Async server
```

</details>

---

## 🚀 Quick Start

### 30-Second Tutorial

```bash
# 1. Scrub a single image
python3 imageghost.py cli scrub image.jpg -o clean.jpg

# 2. Batch scrub a folder
python3 imageghost.py cli scrub /photos -o /clean_photos

# 3. Full pipeline (scrub → encrypt → shred)
python3 imageghost.py cli pipeline /photos -p MySecurePass123!

# 4. Launch web dashboard
python3 imageghost.py web
# Open browser: http://localhost:5000
```

---

## 📖 Usage

### CLI Mode

#### Basic Operations

```bash
# View help
python3 imageghost.py --help
python3 imageghost.py cli --help

# Scrub single image
python3 imageghost.py cli scrub input.jpg -o output.jpg

# Scrub folder
python3 imageghost.py cli scrub /input_folder -o /output_folder

# See metadata before scrubbing
python3 imageghost.py cli scrub input.jpg -o output.jpg --analyze
```

#### Advanced Scrubbing

```bash
# Scrub with encryption
python3 imageghost.py cli scrub /photos -e -p "SecurePassword123!"

# Scrub + encrypt + shred originals (DoD 7-pass)
python3 imageghost.py cli scrub /photos -e -s --shred-method dod -p "Pass123"

# Maximum security (Gutmann 35-pass)
python3 imageghost.py cli scrub /photos -e -s --shred-method gutmann -p "Pass"
```

#### Encryption Operations

```bash
# Encrypt cleaned images
python3 imageghost.py cli encrypt /clean_photos -p "MyPassword"

# Decrypt files
python3 imageghost.py cli decrypt file.enc -o decrypted.jpg -p "MyPassword"

# Batch decrypt
python3 imageghost.py cli decrypt /encrypted_folder -o /output -p "Pass"
```

#### Full Pipeline

```bash
# Complete workflow: scrub → encrypt → shred
python3 imageghost.py cli pipeline /sensitive_photos \
    --shred-originals \
    --shred-method gutmann \
    -p "Ultra-Secure-Password-2024!"

# Generate secure password on the fly
python3 imageghost.py cli pipeline /photos -p "$(openssl rand -base64 32)"
```

### Web Dashboard (GUI Mode)

#### Starting the Dashboard

```bash
# Default (localhost:5000)
python3 imageghost.py web
# or
python3 imageghost.py gui

# Custom port
python3 imageghost.py web --port 8080

# Network accessible (WARNING: Use with caution)
python3 imageghost.py web --host 0.0.0.0 --port 8080

# Debug mode
python3 imageghost.py web --debug
```

**Access:** Open browser to `http://localhost:5000`

#### Dashboard Operations

**Upload & Scrub:**
1. Drag & drop images (or click to select)
2. Choose operation: Scrub, Encrypt, or Full Pipeline
3. Configure settings (shred method, encryption)
4. Click "Process"
5. Watch real-time progress
6. Download cleaned files

**Theme Switching:**
- Click theme icon in sidebar
- Select from 9 professional themes
- Theme persists across sessions

**Job Management:**
- View all active/completed jobs
- Monitor progress in real-time
- Cancel running jobs
- Download results

---

## 🖼️ Supported Formats

**46+ Image Formats**

| Category | Formats | Count |
|----------|---------|-------|
| **Standard Raster** | JPG, JPEG, PNG, GIF, BMP, TIFF, WebP, ICO, SVG | 9 |
| **RAW Camera** | CR2 (Canon), NEF (Nikon), ARW (Sony), DNG (Adobe), ORF (Olympus), RW2 (Panasonic), PEF (Pentax), SRW (Samsung), RAF (Fujifilm) | 9 |
| **Professional** | PSD, PSB (Photoshop), XCF (GIMP), KRA (Krita) | 4 |
| **HDR** | HDR, EXR, PFM | 3 |
| **Legacy** | PCX, TGA, ICNS, JP2, J2K, JPF, JPX | 7 |
| **Medical** | DCM, DICOM | 2 |
| **Misc** | PPM, PGM, PBM, PNM, XBM, XPM | 6 |

**RAW Format Support:**
- ✅ Canon (CR2, CRW)
- ✅ Nikon (NEF, NRW)
- ✅ Sony (ARW, SRF, SR2)
- ✅ Adobe (DNG)
- ✅ Olympus (ORF)
- ✅ Panasonic (RW2)
- ✅ Pentax (PEF)
- ✅ Samsung (SRW)
- ✅ Fujifilm (RAF)

---

## 🔒 Security

### Threat Model

ImageGhost protects against:

| Threat | Protection | Method |
|--------|------------|--------|
| **Metadata Attribution** | ✅ Complete | 4-layer scrubbing |
| **GPS Tracking** | ✅ Complete | GPS tag removal |
| **Device Fingerprinting** | ✅ Complete | Camera info removal |
| **Timestamp Correlation** | ✅ Complete | All timestamps removed |
| **Software Watermarking** | ✅ Complete | Tool signatures removed |
| **Steganography** | ✅ Complete | LSB normalization |
| **Forensic Recovery** | ✅ Complete | DoD/Gutmann shredding |
| **Tampering** | ✅ Detected | AES-GCM AEAD |

### Security Features

<table>
<tr>
<td width="50%">

**Cryptographic:**
- ✅ AES-256-GCM encryption
- ✅ Argon2id key derivation
- ✅ 256-bit secure random salt
- ✅ Authenticated encryption (AEAD)
- ✅ No key material in memory

</td>
<td width="50%">

**Operational:**
- ✅ 100% local processing
- ✅ Zero external connections
- ✅ Memory clearing
- ✅ Verified secure deletion
- ✅ Open source (auditable)

</td>
</tr>
</table>

### Best Practices

```bash
# Maximum paranoia mode
python3 imageghost.py cli pipeline /sensitive \
    --shred-method gutmann \
    --shred-originals \
    -p "$(openssl rand -base64 32)" \
    && shred -vfz -n 35 /path/to/password/file

# Verify originals are gone
ls -la /sensitive  # Should be empty

# Use air-gapped system for maximum security
# Never connect cleaned images to original metadata
# Store encrypted files on separate devices
```

---

## ⚡ Performance

### Benchmarks

**Test System:** Intel i7-9700K, 32GB RAM, NVMe SSD

| Operation | Single Image | 10 Images | 100 Images | Notes |
|-----------|--------------|-----------|------------|-------|
| **Scrub Only** | 0.8s | 3.2s | 28s | 4-layer cleaning |
| **Scrub + Encrypt** | 1.2s | 4.8s | 42s | AES-256-GCM |
| **Full Pipeline (DoD)** | 2.1s | 8.5s | 78s | + 7-pass shred |
| **Full Pipeline (Gutmann)** | 6.8s | 27s | 245s | + 35-pass shred |

**Parallelization:**
- ✅ Multi-threaded image processing
- ✅ Batch operations parallelized
- ✅ CPU-bound operations optimized
- ✅ I/O operations asynchronous

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | 5-minute getting started guide |
| [FEATURES.md](FEATURES.md) | Detailed feature documentation |
| [THEMES.md](THEMES.md) | GUI theme customization guide |
| [INSTALL.md](INSTALL.md) | Comprehensive installation guide |
| [SECURITY.md](SECURITY.md) | Security policy & vulnerability reporting |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines & code of conduct |
| [CHANGELOG.md](CHANGELOG.md) | Version history and changes |

---

## ❓ FAQ

<details>
<summary><b>Is ImageGhost really secure?</b></summary>

Yes. ImageGhost uses industry-standard encryption (AES-256-GCM) with hardened key derivation (Argon2id). All processing is local with zero external connections. The code is open source for full transparency and auditing.

</details>

<details>
<summary><b>Will this work on Windows or macOS?</b></summary>

ImageGhost is designed for Linux. While Python is cross-platform, some system tools (like exiftool paths) are Linux-specific. Community ports to Windows/macOS are welcome!

</details>

<details>
<summary><b>Can forensics still recover my original images?</b></summary>

With DoD 5220.22-M (7-pass) or Gutmann (35-pass) secure deletion, forensic recovery is virtually impossible on modern storage. SSDs with TRIM enabled provide additional security.

</details>

<details>
<summary><b>Does this remove steganography?</b></summary>

Yes! Layer 3 of our cleaning process normalizes LSB (Least Significant Bits) to remove potential hidden steganographic data. However, sophisticated stego may require additional tools.

</details>

<details>
<summary><b>How do I verify metadata is actually removed?</b></summary>

Use the `--analyze` flag to see before/after metadata comparison. You can also use external tools like `exiftool -a -G1 image.jpg` to verify.

</details>

<details>
<summary><b>Can I use this for red team operations?</b></summary>

Yes! ImageGhost is designed for authorized security testing and red team operations. Ensure you have proper authorization before use. It's perfect for OPSEC-compliant image sanitization.

</details>

<details>
<summary><b>What's the difference between CLI and Web dashboard?</b></summary>

Both provide the same functionality. CLI is faster for automation and scripting. Web dashboard provides a modern GUI with drag & drop, real-time progress, and 9 professional themes.

</details>

---

## 🤝 Contributing

We welcome contributions from the security community!

**How to contribute:**

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. ✅ Commit changes (`git commit -m 'Add AmazingFeature'`)
4. 📤 Push to branch (`git push origin feature/AmazingFeature`)
5. 🔄 Open a Pull Request

**Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:**
- Code of Conduct
- Development setup
- Coding standards (Black, Flake8)
- Pull request process
- Issue reporting guidelines

### Development Setup

```bash
# Clone repository
git clone https://github.com/0xArchCrawler/ImageGhost.git
cd ImageGhost

# Install dependencies
pip3 install -r requirements.txt

# Install dev tools
pip3 install pytest black flake8 mypy

# Run tests
./run_tests.sh

# Format code
black .

# Lint code
flake8 .
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**TL;DR:** You can use, modify, and distribute this software freely. Just keep the license notice.

---

## ⚠️ Disclaimer

**FOR PRIVACY PROTECTION AND AUTHORIZED USE ONLY**

ImageGhost is designed for **legitimate** use cases:

<table>
<tr>
<td width="50%">

**✅ Authorized Uses:**
- Personal privacy protection
- Metadata sanitization for public sharing
- Zero-trust security practices
- Authorized security testing & research
- Journalist source protection
- Human rights documentation
- Operational security (OPSEC)
- CTF competitions
- Red team operations (authorized)

</td>
<td width="50%">

**❌ Prohibited Uses:**
- Illegal activities
- Unauthorized access
- Malicious operations
- Evidence tampering
- Law evasion
- Harassment
- Unauthorized data destruction

</td>
</tr>
</table>

### Legal Notice

**Your Privacy, Your Control.**

Users are **solely responsible** for complying with all applicable laws and regulations in their jurisdiction. This tool is provided for **legitimate privacy protection and security purposes only**.

The authors assume **NO liability** for misuse of this tool. By using ImageGhost, you agree to use it only for lawful purposes with proper authorization.

---

## 🌟 Star History

If you find ImageGhost useful, please consider:
- ⭐ **Star this repository** (helps others discover it!)
- 🍴 **Fork & contribute** (PRs welcome!)
- 🐛 **Report bugs** (via Issues)
- 💡 **Suggest features** (via Discussions)
- 📢 **Share with community** (spread the word!)

---

## 📞 Support

### Get Help

- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/0xArchCrawler/ImageGhost/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/0xArchCrawler/ImageGhost/discussions)
- 🔒 **Security:** See [SECURITY.md](SECURITY.md) for vulnerability reporting

### Community

- Star & watch this repository for updates
- Follow development progress
- Join discussions and provide feedback
- Contribute code, documentation, or bug reports

---

## 🔗 Links

- **Repository:** https://github.com/0xArchCrawler/ImageGhost
- **Documentation:** https://github.com/0xArchCrawler/ImageGhost#readme
- **Releases:** https://github.com/0xArchCrawler/ImageGhost/releases
- **Issues:** https://github.com/0xArchCrawler/ImageGhost/issues
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **License:** [MIT License](LICENSE)

---

<div align="center">

**Made with 💀 for Red Teams & Security Professionals**

*ImageGhost v3.0.0 - Professional Metadata Scrubbing & Encryption*

---

### ⭐ If ImageGhost helps you, give it a star!

[![Star History Chart](https://img.shields.io/github/stars/0xArchCrawler/ImageGhost?style=social)](https://github.com/0xArchCrawler/ImageGhost/stargazers)

---

[⬆ Back to Top](#-imageghost)

</div>

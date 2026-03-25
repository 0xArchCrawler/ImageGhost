# imageghost - complete feature list

## core capabilities

### metadata removal
- **exif data**: camera make/model, lens info, focal length, aperture, iso, shutter speed
- **gps coordinates**: latitude, longitude, altitude, gps timestamps
- **timestamps**: date taken, date modified, date digitized
- **camera settings**: white balance, flash, metering mode, exposure program
- **xmp tags**: adobe metadata, lightroom settings, ratings, labels
- **iptc tags**: copyright, keywords, descriptions, creator info
- **thumbnails**: embedded preview images
- **color profiles**: icc profiles
- **software tags**: editing software signatures
- **comments**: user comments and descriptions

### steganography detection & removal
- lsb (least significant bit) normalization
- embedded data detection
- hidden file signatures
- pixel data sanitization

### encryption
- algorithm: aes-256-gcm
- key derivation: argon2id
- parameters:
  - time cost: 4 iterations
  - memory cost: 64 mb
  - parallelism: 4 threads
  - salt length: 256 bits
- authenticated encryption with associated data (aead)
- end-to-end encryption
- password strength verification

### secure deletion
- dod 5220.22-m (7-pass)
- gutmann method (35-pass)
- random data (7-pass)
- quick mode (3-pass)
- filename obscuration
- file truncation
- verified deletion

## supported formats (50+)

### standard raster
- jpeg/jpg (including jfif, jpe)
- png (including apng)
- gif
- bmp/dib
- tiff/tif
- webp
- ico
- svg

### raw camera formats
- cr2 (canon)
- nef (nikon)
- arw (sony)
- dng (adobe)
- orf (olympus)
- rw2 (panasonic)
- pef (pentax)
- srw (samsung)
- raf (fujifilm)
- raw (generic)

### professional formats
- psd/psb (photoshop)
- xcf (gimp)
- kra (krita)

### legacy formats
- pcx
- tga
- icns
- jp2/j2k/jpf/jpx (jpeg2000)

### high dynamic range
- hdr
- exr
- pfm

### medical imaging
- dcm/dicom

### misc formats
- ppm/pgm/pbm/pnm
- xbm/xpm

## web dashboard features (gui)

### themes
- **arch dark**: clean minimal dark theme with blue accents
- **blackarch**: green-on-black terminal style
- **dracula**: purple/pink modern theme
- **gruvbox**: warm retro color scheme
- **green hacker**: matrix-style green theme
- **blue soc**: professional blue theme
- **red team**: aggressive red theme
- **purple team**: combined ops purple theme
- **nord**: arctic blue/white theme

### interface
- modern browser-based ui
- drag & drop file upload
- real-time websocket progress updates
- job management dashboard
- live console logging
- batch file selection
- secure password generation
- theme switching
- status indicators
- multiple concurrent jobs support

### operations
- single file processing
- batch processing (60-100+ files)
- background job threading
- error handling & recovery
- completion notifications
- download processed files as zip
- job history tracking

## cli features

### commands
- `scrub`: remove metadata
- `encrypt`: encrypt files
- `decrypt`: decrypt files
- `pipeline`: full workflow

### options
- verbose output
- encryption after scrubbing
- secure deletion
- shred method selection
- output directory specification
- password via argument or prompt

### workflows
- scrub only
- scrub + encrypt
- scrub + encrypt + shred
- encrypt existing files
- decrypt files
- full automated pipeline

## batch processing

### performance
- handles 60-100+ images simultaneously
- parallel processing support
- progress tracking
- error recovery
- statistics reporting

### output
- processed file count
- failed file count
- bytes of metadata removed
- processing time
- individual file results

## security features

### metadata removal layers
1. pil complete rewrite (removes most metadata)
2. exiftool nuclear clean (removes everything)
3. steganography trace removal
4. image re-encoding

### encryption security
- military-grade aes-256-gcm
- hardened argon2id kdf
- cryptographically secure random nonces
- authenticated encryption
- password strength validation
- secure password generation (32 chars)

### secure deletion security
- multiple overwrite passes
- random data generation
- pattern-based overwrites
- filename randomization
- file truncation
- verification

## use cases

### operational security
- remove identifying metadata from reconnaissance photos
- sanitize screenshots before sharing
- clean exfil images
- prepare images for covert channels

### red team operations
- sanitize payload delivery images
- clean phishing campaign graphics
- remove forensic traces
- prepare social engineering materials

### penetration testing
- clean proof-of-concept images
- sanitize report screenshots
- remove client-identifying data
- prepare evidence for delivery

### ctf competitions
- clean challenge images
- remove metadata hints
- sanitize team communications
- prepare writeup screenshots

## technical details

### architecture
```
imageghost/
├── core/               # core processing modules
│   ├── scrubber.py     # metadata removal engine
│   ├── crypto.py       # encryption engine
│   ├── secure_delete.py # shredding engine
│   └── formats.py      # format detection
├── cli/                # command-line interface
├── gui/                # graphical interface
│   └── themes.py       # theme definitions
└── imageghost.py       # main entry point
```

### dependencies
- pillow: image processing
- cryptography: encryption
- pyqt5: gui framework
- argon2-cffi: key derivation
- pycryptodome: crypto operations

### system requirements
- python 3.7+
- linux (arch, kali, ubuntu, debian)
- optional: exiftool for enhanced scrubbing
- optional: dcraw for raw format support

## code statistics
- total lines: ~2,255
- modules: 9
- themes: 4
- supported formats: 50+
- security layers: 4

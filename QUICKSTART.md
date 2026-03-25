# imageghost - quick start guide

## instant setup

```bash
cd /home/stuxnet/MyTools/ImageGhost
pip3 install -r requirements.txt
```

## fastest way to use

### web dashboard (gui - recommended for beginners)

```bash
python3 imageghost.py gui
# opens web browser at http://localhost:5000
```

1. drag & drop images or click to upload
2. select operation (scrub, encrypt, pipeline)
3. choose options (encrypt, shred method)
4. enter password if encrypting
5. click "start" and watch real-time progress
6. download results when complete

### cli (for batch operations)

```bash
# scrub all images in a folder
python3 imageghost.py cli scrub /path/to/folder -o /path/to/output

# scrub + encrypt + delete originals
python3 imageghost.py cli pipeline /path/to/folder --shred-originals -p password123
```

## common commands

### just remove metadata

```bash
python3 imageghost.py cli scrub ~/pictures -o ~/cleaned_pictures
```

### remove metadata + encrypt

```bash
python3 imageghost.py cli scrub ~/pictures -e -p mypassword
```

### full secure workflow

```bash
python3 imageghost.py cli pipeline ~/sensitive_pics \\
    --shred-originals \\
    --shred-method dod \\
    -p "strong-password-here"
```

## what it does

1. **scrub**: removes ALL metadata (exif, gps, timestamps, camera info, thumbnails, everything)
2. **encrypt**: uses military-grade aes-256-gcm encryption
3. **shred**: securely deletes original files (dod 5220.22-m standard)

## web dashboard themes

change theme in settings section:
- arch dark (default)
- blackarch (green terminal)
- dracula (purple/pink)
- gruvbox (warm retro)
- green hacker (matrix)
- blue soc (professional blue)
- red team (aggressive red)
- purple team (combined ops)
- nord (arctic blue)

## tips

- supports 50+ image formats
- batch process 100+ images at once
- all operations are irreversible (by design)
- keep encrypted files safe - no password recovery

## help

```bash
python3 imageghost.py cli --help
python3 imageghost.py cli scrub --help
python3 imageghost.py cli encrypt --help
python3 imageghost.py cli pipeline --help
```

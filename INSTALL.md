# imageghost v3.0 - installation guide

## quick install

```bash
cd /home/stuxnet/MyTools/ImageGhost
pip3 install -r requirements.txt
```

## dependencies

### required python packages
```bash
pip3 install Pillow cryptography argon2-cffi pycryptodome flask flask-socketio python-socketio
```

### optional system tools (for enhanced scrubbing)
```bash
# debian/ubuntu/kali
sudo apt install exiftool dcraw steghide binwalk

# arch linux
sudo pacman -S perl-image-exiftool dcraw steghide binwalk

# fedora
sudo dnf install perl-Image-ExifTool dcraw steghide binwalk
```

## verification

```bash
# test core modules
python3 -c "from core.scrubber import ImageScrubber; print('✓ scrubber OK')"
python3 -c "from core.crypto import ImageCrypto; print('✓ crypto OK')"
python3 -c "from core.secure_delete import SecureDelete; print('✓ secure delete OK')"

# test cli
python3 imageghost.py cli --help

# test web dashboard (opens browser at localhost:5000)
python3 imageghost.py gui
```

## first run

### cli mode
```bash
# create test directory
mkdir -p ~/test_images
# add some test images
# then run
python3 imageghost.py cli scrub ~/test_images -o ~/cleaned_images
```

### web dashboard mode
```bash
python3 imageghost.py gui
# access at http://localhost:5000
```

## troubleshooting

### missing dependencies
```bash
pip3 install -r requirements.txt --upgrade
```

### flask/socketio issues
```bash
pip3 install --upgrade flask flask-socketio python-socketio werkzeug
```

### exiftool not found
```bash
# the tool works without exiftool but with reduced functionality
sudo apt install exiftool  # debian/ubuntu/kali
sudo pacman -S perl-image-exiftool  # arch linux
```

### permission errors
```bash
chmod +x imageghost.py
chmod +x cli/imageghost_cli.py
```

## creating alias (optional)

add to ~/.bashrc or ~/.zshrc:
```bash
alias imageghost='python3 /home/stuxnet/MyTools/ImageGhost/imageghost.py'
```

then use:
```bash
imageghost cli scrub ~/images
imageghost gui
```

## docker installation (optional)

create Dockerfile:
```dockerfile
FROM kalilinux/kali-rolling
RUN apt update && apt install -y python3 python3-pip exiftool
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "imageghost.py"]
```

build and run:
```bash
docker build -t imageghost .
docker run -it -v ~/images:/images imageghost cli scrub /images
```

## uninstall

```bash
# remove tool
rm -rf /home/stuxnet/MyTools/ImageGhost

# remove python packages (optional)
pip3 uninstall Pillow cryptography argon2-cffi pycryptodome flask flask-socketio python-socketio
```

## update

```bash
cd /home/stuxnet/MyTools/ImageGhost
git pull  # if using git
pip3 install -r requirements.txt --upgrade
```

## support

- documentation: README.md
- quick start: QUICKSTART.md
- features: FEATURES.md
- themes: THEMES.md

# Image format handlers
# Supports pretty much every image format out there

import os
from PIL import Image
import struct

# massive list of supported formats
FORMATS = {
    # standard raster
    '.jpg': 'JPEG',
    '.jpeg': 'JPEG',
    '.jpe': 'JPEG',
    '.jfif': 'JPEG',
    '.png': 'PNG',
    '.apng': 'PNG',
    '.gif': 'GIF',
    '.bmp': 'BMP',
    '.dib': 'BMP',
    '.tif': 'TIFF',
    '.tiff': 'TIFF',

    # web formats
    '.webp': 'WEBP',
    '.svg': 'SVG',
    '.ico': 'ICO',

    # raw camera formats
    '.cr2': 'RAW',  # canon
    '.nef': 'RAW',  # nikon
    '.arw': 'RAW',  # sony
    '.dng': 'RAW',  # adobe
    '.orf': 'RAW',  # olympus
    '.rw2': 'RAW',  # panasonic
    '.pef': 'RAW',  # pentax
    '.srw': 'RAW',  # samsung
    '.raf': 'RAW',  # fuji
    '.raw': 'RAW',  # generic

    # professional formats
    '.psd': 'PSD',  # photoshop
    '.psb': 'PSD',  # photoshop large
    '.xcf': 'XCF',  # gimp
    '.kra': 'KRA',  # krita

    # old school formats
    '.pcx': 'PCX',
    '.tga': 'TGA',
    '.icns': 'ICNS',
    '.jp2': 'JPEG2000',
    '.j2k': 'JPEG2000',
    '.jpf': 'JPEG2000',
    '.jpx': 'JPEG2000',

    # high dynamic range
    '.hdr': 'HDR',
    '.exr': 'EXR',
    '.pfm': 'PFM',

    # medical imaging
    '.dcm': 'DICOM',
    '.dicom': 'DICOM',

    # misc
    '.ppm': 'PPM',
    '.pgm': 'PGM',
    '.pbm': 'PBM',
    '.pnm': 'PNM',
    '.xbm': 'XBM',
    '.xpm': 'XPM',
}

def check_format(filepath):
    """check if we can handle this file"""
    ext = os.path.splitext(filepath)[1].lower()
    return ext in FORMATS

def get_format_name(filepath):
    """get the format name"""
    ext = os.path.splitext(filepath)[1].lower()
    return FORMATS.get(ext, 'UNKNOWN')

def convert_to_standard(input_path, output_path):
    """
    converts weird formats to standard jpeg for processing
    this is needed for raw camera files and other exotic formats
    """
    try:
        # try opening with PIL first
        img = Image.open(input_path)

        # convert to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            # handle transparency
            bg = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            if 'A' in img.mode:
                bg.paste(img, mask=img.split()[-1])
            else:
                bg.paste(img)
            img = bg
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # save as jpeg with no metadata
        img.save(output_path, 'JPEG', quality=95, exif=b'')
        return True

    except (IOError, OSError) as e:
        # fallback for raw formats - use dcraw if available
        try:
            import subprocess
            with open(output_path, 'wb') as out_file:
                subprocess.run(['dcraw', '-c', '-w', input_path],
                             stdout=out_file,
                             stderr=subprocess.DEVNULL,
                             timeout=60,
                             check=True)
            return True
        except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.CalledProcessError):
            return False

def batch_check_formats(directory):
    """scan directory and categorize files by format"""
    stats = {}
    supported = []
    unsupported = []

    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        if not os.path.isfile(path):
            continue

        ext = os.path.splitext(f)[1].lower()

        if ext in FORMATS:
            fmt = FORMATS[ext]
            stats[fmt] = stats.get(fmt, 0) + 1
            supported.append(f)
        else:
            unsupported.append(f)

    return {
        'stats': stats,
        'supported': supported,
        'unsupported': unsupported,
        'total': len(supported) + len(unsupported)
    }

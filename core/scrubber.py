# metadata scrubbing engine
# handles all the dirty work of removing every trace from images

import os
import io
import subprocess
from PIL import Image
from typing import List, Dict, Optional, Tuple
import tempfile
import shutil
import json


class ImageScrubber:
    """removes all metadata from images - exif, gps, xmp, iptc, thumbnails, everything"""

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.stats = {
            'processed': 0,
            'failed': 0,
            'bytes_removed': 0
        }

    def scrub_image(self, input_path, output_path):
        """scrub a single image clean"""
        try:
            if self.verbose:
                print(f"[*] scrubbing: {os.path.basename(input_path)}")

            # Extract metadata BEFORE cleaning
            before_metadata = self._extract_metadata(input_path)

            # step 1: PIL complete rewrite (gets most metadata)
            self._pil_scrub(input_path, output_path)

            # step 2: exiftool nuclear option if available
            self._exiftool_scrub(output_path)

            # step 3: strip any steganography traces
            self._strip_stego_traces(output_path)

            # step 4: re-encode to ensure clean state
            self._reencode_image(output_path)

            # Extract metadata AFTER cleaning
            after_metadata = self._extract_metadata(output_path)

            # Calculate changes
            bytes_removed = before_metadata['file_size'] - after_metadata['file_size']
            exif_removed = before_metadata['exif_count'] - after_metadata['exif_count']

            self.stats['processed'] += 1
            self.stats['bytes_removed'] += bytes_removed

            if self.verbose:
                print(f"[+] removed {bytes_removed} bytes of metadata")

            return True, {
                'before': before_metadata,
                'after': after_metadata,
                'bytes_removed': bytes_removed,
                'exif_removed': exif_removed,
                'success': True,
                # Keep old format for backward compatibility
                'original_metadata': before_metadata['raw_tags']
            }

        except Exception as e:
            self.stats['failed'] += 1
            if self.verbose:
                print(f"[-] failed to scrub {input_path}: {str(e)}")
            return False, {'success': False, 'error': str(e)}

    def _pil_scrub(self, input_path, output_path):
        """use PIL to completely rewrite image without metadata"""
        with Image.open(input_path) as img:
            # convert to RGB if needed
            if img.mode not in ('RGB', 'L'):
                if img.mode == 'RGBA':
                    # white background for transparency
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3] if len(img.split()) > 3 else None)
                    img = background
                else:
                    img = img.convert('RGB')

            # create completely new image with no metadata
            clean_img = Image.new(img.mode, img.size)
            clean_img.putdata(list(img.getdata()))

            # save with no exif, no metadata
            clean_img.save(output_path, quality=95, optimize=True, exif=b'')

    def _exiftool_scrub(self, file_path):
        """use exiftool to remove ALL metadata tags"""
        try:
            # nuclear option: remove everything
            cmd = [
                'exiftool',
                '-all=',
                '-thumbnails:all=',
                '-preview:all=',
                '-Adobe:all=',
                '-XMP:all=',
                '-IPTC:all=',
                '-ICC_Profile:all=',
                '-Photoshop:all=',
                '-overwrite_original',
                '-q',
                file_path
            ]

            subprocess.run(cmd, check=True, timeout=30,
                         stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.CalledProcessError):
            # exiftool not available or failed, PIL already did most work
            pass

    def _strip_stego_traces(self, file_path):
        """remove potential steganography traces by normalizing LSBs"""
        try:
            with Image.open(file_path) as img:
                pixels = img.load()
                width, height = img.size

                # normalize LSBs in pixel data
                for y in range(height):
                    for x in range(width):
                        if img.mode == 'RGB':
                            r, g, b = pixels[x, y]
                            # zero out LSB of each channel
                            pixels[x, y] = (r & 0xFE, g & 0xFE, b & 0xFE)
                        elif img.mode == 'L':
                            pixels[x, y] = pixels[x, y] & 0xFE

                img.save(file_path, quality=95, optimize=True)

        except (IOError, OSError) as e:
            # Failed to strip stego traces, continue anyway
            if self.verbose:
                print(f"[!] Warning: Could not strip steganography traces: {e}")

    def _reencode_image(self, file_path):
        """re-encode image to ensure clean state"""
        try:
            with Image.open(file_path) as img:
                temp_fd, temp_path = tempfile.mkstemp(suffix='.jpg')
                os.close(temp_fd)

                img.save(temp_path, 'JPEG', quality=95, optimize=True, exif=b'')
                shutil.move(temp_path, file_path)

        except (IOError, OSError) as e:
            # Re-encoding failed, original cleaned image is still valid
            if self.verbose:
                print(f"[!] Warning: Could not re-encode image: {e}")

    def _extract_metadata(self, file_path):
        """extract detailed metadata for logging"""
        metadata = {
            'raw_tags': {},
            'format': 'Unknown',
            'dimensions': (0, 0),
            'file_size': 0,
            'exif_count': 0,
            'has_icc_profile': False,
            'has_gps': False,
            'has_thumbnail': False
        }

        try:
            # Get file size
            metadata['file_size'] = os.path.getsize(file_path)

            # Get image info using PIL
            with Image.open(file_path) as img:
                metadata['format'] = img.format or 'Unknown'
                metadata['dimensions'] = img.size

                # Check for ICC profile
                if 'icc_profile' in img.info:
                    metadata['has_icc_profile'] = True

            # Try exiftool for detailed tags
            cmd = ['exiftool', '-json', '-a', '-G', file_path]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, timeout=10, text=True,
                                  stderr=subprocess.DEVNULL)

            if result.returncode == 0:
                data = json.loads(result.stdout)
                if data:
                    raw_data = data[0]
                    metadata['raw_tags'] = raw_data

                    # Count EXIF fields (exclude basic file info)
                    exif_fields = {k: v for k, v in raw_data.items()
                                  if not k.startswith('File:') and
                                  not k.startswith('SourceFile')}
                    metadata['exif_count'] = len(exif_fields)

                    # Check for GPS data
                    metadata['has_gps'] = any('GPS' in k for k in raw_data.keys())

                    # Check for thumbnail
                    metadata['has_thumbnail'] = any('Thumbnail' in k for k in raw_data.keys())

        except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
            # exiftool not available, use PIL only
            pass
        except (IOError, OSError):
            pass

        return metadata

    def batch_scrub(self, input_dir, output_dir, file_list=None):
        """batch scrub multiple images"""
        os.makedirs(output_dir, exist_ok=True)

        from core.formats import check_format

        if file_list is None:
            file_list = [f for f in os.listdir(input_dir)
                        if check_format(os.path.join(input_dir, f))]

        results = []
        total = len(file_list)

        print(f"\n[*] processing {total} images...")
        print("=" * 60)

        for idx, filename in enumerate(file_list, 1):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            print(f"\n[{idx}/{total}] processing: {filename}")

            success, info = self.scrub_image(input_path, output_path)
            results.append({
                'filename': filename,
                'success': success,
                'info': info
            })

        print("\n" + "=" * 60)
        print(f"\n[+] batch complete!")
        print(f"    processed: {self.stats['processed']}")
        print(f"    failed: {self.stats['failed']}")
        print(f"    total metadata removed: {self.stats['bytes_removed']:,} bytes")

        return {
            'stats': self.stats,
            'results': results
        }

    def get_stats(self):
        """get scrubbing statistics"""
        return self.stats.copy()

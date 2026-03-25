"""
ImageGhost - Multi-Image Fingerprint Scrubber
Professional-grade metadata removal and encryption for pentesters/red-teamers
"""

__version__ = "1.0.0"
__author__ = "ImageGhost Security Team"

from .scrubber import ImageScrubber
from .crypto import ImageCrypto
from .secure_delete import SecureDelete

__all__ = ['ImageScrubber', 'ImageCrypto', 'SecureDelete']

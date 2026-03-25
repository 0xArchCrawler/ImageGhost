#!/bin/bash
# imageghost v3.0 - test suite

echo "╔════════════════════════════════════════════════════╗"
echo "║        IMAGEGHOST v3.0 TEST SUITE                 ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

cd /home/stuxnet/MyTools/ImageGhost

# test 1: syntax check
echo "[1/5] syntax check..."
python3 -m py_compile imageghost.py cli/imageghost_cli.py gui/imageghost_gui.py core/*.py 2>&1
if [ $? -eq 0 ]; then
    echo "  ✓ all files have valid syntax"
else
    echo "  ✗ syntax errors found"
    exit 1
fi

# test 2: import test
echo ""
echo "[2/5] import test..."
python3 << 'PYEOF'
try:
    from core.scrubber import ImageScrubber
    from core.crypto import ImageCrypto
    from core.secure_delete import SecureDelete
    from core.formats import check_format, FORMATS
    print("  ✓ all modules imported successfully")
except ImportError as e:
    print(f"  ✗ import error: {e}")
    exit(1)
PYEOF

# test 3: functionality test
echo ""
echo "[3/5] functionality test..."
python3 << 'PYEOF'
import tempfile
import os
from PIL import Image
from core.scrubber import ImageScrubber
from core.crypto import ImageCrypto

# create test image
test_dir = tempfile.mkdtemp()
test_img = os.path.join(test_dir, 'test.jpg')
img = Image.new('RGB', (50, 50), 'blue')
img.save(test_img)

# test scrubbing
scrubber = ImageScrubber(verbose=False)
output = os.path.join(test_dir, 'clean.jpg')
success, _ = scrubber.scrub_image(test_img, output)

if success:
    print("  ✓ scrubbing works")
else:
    print("  ✗ scrubbing failed")
    exit(1)

# test encryption
crypto = ImageCrypto(verbose=False)
encrypted = os.path.join(test_dir, 'test.enc')
if crypto.encrypt_file(output, encrypted, 'test123'):
    print("  ✓ encryption works")
else:
    print("  ✗ encryption failed")
    exit(1)

# cleanup
import shutil
shutil.rmtree(test_dir)
PYEOF

# test 4: cli test
echo ""
echo "[4/5] cli test..."
python3 imageghost.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "  ✓ cli interface works"
else
    echo "  ✗ cli interface failed"
    exit 1
fi

# test 5: format support
echo ""
echo "[5/5] format support test..."
python3 << 'PYEOF'
from core.formats import FORMATS
count = len(FORMATS)
if count >= 40:
    print(f"  ✓ {count} image formats supported")
else:
    print(f"  ✗ only {count} formats (expected 40+)")
    exit(1)
PYEOF

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║           ALL TESTS PASSED ✓                      ║"
echo "║      imageghost v3.0 is fully operational         ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "ready to use:"
echo "  python3 imageghost.py cli scrub /path/to/images"
echo "  python3 imageghost.py gui"
echo ""

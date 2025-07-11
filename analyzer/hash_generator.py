import hashlib
import imagehash
from PIL import Image

def generate_sha256(file_path):
    """Generates the SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_phash(file_path):
    """Generates the perceptual hash (pHash) of an image."""
    try:
        with Image.open(file_path) as img:
            return str(imagehash.phash(img))
    except Exception as e:
        return f"Error generating pHash: {e}"

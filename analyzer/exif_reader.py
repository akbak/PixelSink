import exifread

def read_exif_data(file_path):
    """Reads EXIF metadata from an image file."""
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f, details=False)
    
    exif_data = {}
    if not tags:
        return {"Status": "No EXIF information found."}

    for tag, value in tags.items():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail'):
            tag_name = str(tag)
            tag_value = str(value)
            exif_data[tag_name] = tag_value
            
    return exif_data

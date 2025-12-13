
"""
Helper functions to create mock zip files for testing
"""

import zipfile
from io import BytesIO

def create_simple_zip():
    """Make a basic zip with one .dat file"""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        zf.writestr("data.dat", "Sample data content")
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def create_multi_file_zip():
    """Make a zip with multiple files including a .dat file"""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        zf.writestr("readme.txt", "This is a readme")
        zf.writestr("data.dat", "actual data content")
        zf.writestr("metadata.json", '{"version": "1.0"}')
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


if __name__ == "__main__":
    print("Testing zip generators...")
    
    # test simple zip
    simple = create_simple_zip()
    print(f"Simple zip created: {len(simple)} bytes")
    
    # test multi file zip
    multi = create_multi_file_zip()
    print(f"Multi-file zip created: {len(multi)} bytes")

    
    print("All generators working!")
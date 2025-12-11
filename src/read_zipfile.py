import os
import zipfile
import requests
from io import BytesIO


def read_zipfile(url, data_dir):
    """  
    Downloads the zip file from the specified URL, saves it to the data directory,
    and extracts the .dat file contained within.

    Parameters:
    ----------
    url : str
        The URL of the zip file to be read.
    data_dir : str
        The directory where the contents of the zip file will be extracted.

    Returns:
    -------
    None
    """
    
    os.makedirs(data_dir, exist_ok=True)
    
  
    response = requests.get(url)

    
    zip_bytes = BytesIO(response.content)
    
    with zipfile.ZipFile(zip_bytes, "r") as zip_ref:
        dat_files = [f for f in zip_ref.namelist() if f.endswith(".dat")]
        dat_content = zip_ref.read(dat_files[0]).decode("utf-8")
        dat_filename = os.path.basename(dat_files[0])
        
        output_path = os.path.join(data_dir, dat_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(dat_content)
        
        print(f"✓ Downloaded and saved: {output_path}")
        print(f"✓ Extracted .dat file: {dat_filename}")
        print(f"✓ Dataset ready for processing")
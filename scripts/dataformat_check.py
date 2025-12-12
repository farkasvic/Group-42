# scripts/data_validation.py

import os
import pandas as pd
import sys
from pathlib import Path

# Add the 'src' directory to the path so we can import modules from it
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))


from src import check_csv

def main(cleaned_data):
    """
    Validates the input file path format and then reads the data.

    Parameters
    ----------
    cleaned_data : str
        The file path to the cleaned data CSV.
    """
    
    # Define expected values
    correct_filename = "clean_diabetes.csv"
    correct_extension = ".csv"

    try:
        # Call the new function: check_csv
        check_csv(
            filepath=cleaned_data,
            expected_filename=correct_filename, 
            expected_extension=correct_extension
        )
        
        print("Name validation and File format passed.")
        
    except AssertionError as e:
       
        print(f"File validation failed: {e}")
        return
    
    diabetes_df = pd.read_csv(cleaned_data)
    
    print(f"File has been successfully loaded.")

if __name__ == "__main__":
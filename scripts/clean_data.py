"""
Data Cleaning script.

Reads in the .dat file from the data/raw directory, splits by comma delimiter, renames columns, 
converts to proper datatypes, and saves as CSV into data/processed.
  
"""


import pandas as pd
import os
import click

@click.command()
@click.option(
    '--input-path',
    type=str,
    default='data/raw/diabetes.dat',
    help='Path to the raw .dat file'
)
@click.option(
    '--output-dir',
    type=str,
    default='data/processed',
    help='Directory to save the cleaned data'
)
@click.option(
    '--output-file',
    type=str,
    default='clean_diabetes.csv',
    help='Filename for the cleaned CSV file'
)

def main(input_path, output_dir, output_file):

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        dat_content = f.read()

    lines = dat_content.splitlines()
    data_lines = [line for line in lines 
                  if not line.startswith("@") and line.strip()]
    
    rows = [line.strip().split(",") for line in data_lines]

    #data processing

    diabetes_df = pd.DataFrame(rows)
    diabetes_df.columns = ["Age", "Deficit", "C_peptide"]
    diabetes_df = diabetes_df.astype(float)

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, output_file)
   
    diabetes_df.to_csv(output_path, index=False)

 
    print("Data Cleaning Summary")
    print("="*60)
    print(f"✓ Input file: {input_path}")
    print(f"✓ Output file: {output_path}")
    print(f"✓ Rows: {len(diabetes_df)}")
    print(f"✓ Columns: {list(diabetes_df.columns)}")
    print(f"✓ Data types: {diabetes_df.dtypes.to_dict()}")
    print(f"\nFirst few rows:")
    print(diabetes_df.head())

if __name__ == '__main__':
    main()
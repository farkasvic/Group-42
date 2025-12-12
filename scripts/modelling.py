"""
Fits linear regression model on cleaned data. Saves the model to a pickle file and model 
output to a .csv file.
"""

import click
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.lin_reg import lin_reg

@click.command()

@click.option('--cleaned-data', 'cleaned_data', type=click.Path(exists=True),
              default="data/processed/clean_diabetes.csv", help="Path to read in cleaned data")

@click.option('--model-output', 'model_output', type = click.Path(exists=True),
              default = 'results/models', help='Directory models will be output to')

@click.option('--table-output', 'table_output', type = click.Path(exists=True),
              default = 'results/tables', help = 'Directory tables will be output to')

def main(cleaned_data, model_output, table_output):

    lin_reg(
        csv=cleaned_data,
        target="C_peptide",
        model_dir=model_output,
        model_name="lr_model.pickle",
        table_dir=table_output,
        table_name="model_summary.csv"
    )



if __name__ == "__main__":
    main()
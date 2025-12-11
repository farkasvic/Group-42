"""
Data Validation script.

Checks the dataset schema, ranges, and uses the deepchecks data validation suite to run full data
integrity checks. Also checks the file is named correctly and uses the correct format (.csv).

"""



import os
import pandas as pd
import pandera as pa
import click

from pandera import Column, DataFrameSchema, Check
from deepchecks.tabular import Dataset
from deepchecks.tabular.suites import data_integrity

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


expected_columns = ["Age", "Deficit", "C_peptide"]

schema_basic = DataFrameSchema(
    columns={
        "Age": Column(float, nullable=False),
        "Deficit": Column(float, nullable=False),
        "C_peptide": Column(float, nullable=False),
    },
    checks=[
        Check(
            lambda df: (df.isnull().mean() <= 0.05).all(),
            error="Missingness exceeds 5% in some columns",
        )
    ],
    strict=True,
)


# Second schema: value ranges and duplicate check
schema_ranges = DataFrameSchema(
    {
        "Age": pa.Column(float, pa.Check.between(0.9, 15.6)),
        "Deficit": pa.Column(float, pa.Check.between(-29.0, -0.2)),
        "C_peptide": pa.Column(float, pa.Check.between(3.0, 6.6)),
    },
    checks=[
        pa.Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found.")
    ],
    strict=True,
)

@click.command()
@click.option('--cleaned-data', 'cleaned_data', type=click.Path(exists=True),
              default="data/processed/clean_diabetes.csv", help="Path to read in cleaned data")


def main(cleaned_data):

    try:
        actual_filename = os.path.basename(cleaned_data)
        actual_extension = os.path.splitext(actual_filename)[1]
        
        assert actual_filename == "clean_diabetes.csv", \
            f"Expected filename 'clean_diabetes.csv', but got '{actual_filename}'"
        
        assert actual_extension == ".csv", \
            f"Expected file extension '.csv', but got '{actual_extension}'"
        
        print("✅ File format and name validation passed.")
    except AssertionError as e:
        print(f"❌ File validation failed: {e}")
        return
  
    diabetes_df = pd.read_csv(cleaned_data)

    # Validate
    try:
        schema_basic.validate(diabetes_df)
        print("✅ Basic schema validation passed (columns, types, missingness).")
    except Exception as e:
        print(f"Basic schema validation failed: {e}")


    try:
        # Deepchecks validation
        ds_diabetes = Dataset(diabetes_df, label="C_peptide", cat_features=[])
        suite = data_integrity()
        suite.run(ds_diabetes)  # just run, no HTML output

        print("✅ Data validation suite passed.")
    except Exception as e:
        print(f"Data validation failed: {e}")


    try:
        schema_ranges.validate(diabetes_df)
        print("✅ Range and duplicate checks passed.")
    except Exception as e:
        print(f"Range/duplicate validation failed: {e}")


if __name__ == "__main__":
    main()





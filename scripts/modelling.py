import click
import os
import pandas as pd
import pingouin as pg
import pickle


@click.command()

@click.option('--cleaned-data', 'cleaned_data', type=click.Path(exists=True),
              default="data/processed/clean_diabetes.csv", help="Path to read in cleaned data")

@click.option('--model-output', 'model_output', type = click.Path(exists=True),
              default = 'results/models', help='Directory models will be output to')

@click.option('--table-output', 'table_output', type = click.Path(exists=True),
              default = 'results/tables', help = 'Directory tables will be output to')

def main(cleaned_data, model_output, table_output):
    '''
    Fits linear regression model on cleaned data. Saves the model to a pickle file and model 
    output to a .csv file.
    '''

    diabetes_df = pd.read_csv(cleaned_data)

    X = diabetes_df.drop(columns=["C_peptide"])
    y = diabetes_df["C_peptide"]

    model = pg.linear_regression(X, y)
    resid = model.residuals_

    with open(os.path.join(model_output, "lr_model.pickle"), "wb") as f:
        pickle.dump({'results': model, 'residuals': resid}, f)

    with open(os.path.join(table_output, "model_summary.csv"), "w") as f:

        f.write(pd.DataFrame(model).round(3).to_csv())



if __name__ == "__main__":
    main()
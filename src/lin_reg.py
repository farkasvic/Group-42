"""
Fits linear regression model. Saves the model to a pickle file and model 
output to a .csv file.
"""

import os  
import pandas as pd
import pingouin as pg
import pickle

def lin_reg(csv, target, model_dir, model_name, table_dir, table_name):
    """
    Fits and saves information from a linear regression model.

    Parameters:
    -----------
    csv: str
        The file path to the .csv file containing the data.
    target: str
        The name of the target for the linear regression.
    model_dir: str
        The directory where the model's pickle file is saved.
    model_name: str
        The name of the pickle file saved to model_dir. Must end with .pickle.
    table_dir: str
        The directory where the summary table is saved.
    table_name: str
        The name of the summary table saved to table_dir. Must end with .csv.

    Returns:
    ---------
    None

    """

    if not model_name.endswith('.pickle'):
        raise ValueError("model_name must end with .pickle")

    if not table_name.endswith('.csv'):
        raise ValueError("table_name must end with .csv")
    
    df = pd.read_csv(csv)

    X = df.drop(columns=[target])
    y = df[target]

    model = pg.linear_regression(X, y)
    resid = model.residuals_

    with open(os.path.join(model_dir, model_name), "wb") as f:
        pickle.dump({'results': model, 'residuals': resid}, f)
    
    print(f"Saved {model_dir}/{model_name}.")

    with open(os.path.join(table_dir, table_name), "w") as f:
        f.write(pd.DataFrame(model).round(4).to_csv())
    
    print(f"Saved {table_dir}/{table_name}.")

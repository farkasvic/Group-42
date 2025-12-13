import pandas as pd
from deepchecks.tabular import Dataset
from deepchecks.tabular.suites import data_integrity


def run_deepchecks_integrity(df: pd.DataFrame, label: str):
    """
    Run data validation suite on a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe to validate.
    label : str
        Name of the label column.

    Returns
    -------
    Suite result if validation passes.

    Raises
    ------
    ValueError
        If label column is missing.
    Exception
        If Deepchecks fails for any reason.
    """
    if label not in df.columns:
        raise ValueError(f"Label column '{label}' not found in dataframe.")

    ds = Dataset(df, label=label, cat_features=[])
    suite = data_integrity()
    result = suite.run(ds)

    return result


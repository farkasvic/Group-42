import pandas as pd
import pytest
from src.deepchecks_utils import run_deepchecks_integrity
from deepchecks.core.errors import ValidationError

def test_deepchecks_runs_on_valid_data():
    df = pd.DataFrame({
        "Age": [5.0, 10.0],
        "Deficit": [-10.0, -5.0],
        "C_peptide": [4.5, 5.0],
    })

    result = run_deepchecks_integrity(df, label="C_peptide")

    assert result is not None

def test_deepchecks_fails_on_single_row():
    df = pd.DataFrame({
        "Age": [9.0],
        "Deficit": [-7.0],
        "C_peptide": [4.9],
    })

    with pytest.raises(ValidationError):
        run_deepchecks_integrity(df, label="C_peptide")
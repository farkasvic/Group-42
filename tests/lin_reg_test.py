"""
Tests for the lin_reg function.
"""
import os
import sys
import pytest
import pandas as pd
import numpy as np
import pickle
import tempfile
import shutil
from unittest.mock import patch

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.lin_reg import lin_reg


@pytest.fixture
def temp_dirs():
    """Create temporary directories for model and table outputs."""
    model_dir = tempfile.mkdtemp()
    table_dir = tempfile.mkdtemp()
    yield model_dir, table_dir
    shutil.rmtree(model_dir)
    shutil.rmtree(table_dir)


@pytest.fixture
def sample_data():
    """Create a sample CSV file with synthetic data."""
    temp_csv = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
    df = pd.DataFrame({
        "target": [1, 2, 3, 4],
        "predictor": [1, 2, 3, 4]
    })
    df.to_csv(temp_csv.name, index=False)
    temp_csv.close()
    yield temp_csv.name
    os.unlink(temp_csv.name)


def test_dir(sample_data, temp_dirs):
    """Test that pickle and csv files are saved in the correct directories."""
    model_dir, table_dir = temp_dirs
    model_name = "test_model.pickle"
    table_name = "test_table.csv"
    
    lin_reg(sample_data, 'target', model_dir, model_name, table_dir, table_name)
    
    assert os.path.exists(os.path.join(model_dir, model_name))
    assert os.path.exists(os.path.join(table_dir, table_name))

    
def test_residuals(sample_data, temp_dirs):
    """Test that the pickle file contains the expected model and residuals."""
    model_dir, table_dir = temp_dirs
    model_name = "test_model.pickle"
    table_name = "test_table.csv"
    
    lin_reg(sample_data, 'target', model_dir, model_name, table_dir, table_name)
    
    with open(os.path.join(model_dir, model_name), "rb") as f:
        saved_data = pickle.load(f)
    
    assert np.allclose(saved_data['residuals'], np.zeros(4), atol=0.01)


def test_summary(sample_data, temp_dirs):
    """Test that the CSV file contains valid regression results."""
    model_dir, table_dir = temp_dirs
    model_name = "test_model.pickle"
    table_name = "test_table.csv"
    
    lin_reg(sample_data, 'target', model_dir, model_name, table_dir, table_name)
    
    results_df = pd.read_csv(os.path.join(table_dir, table_name))
    
    # Get coefficient values from the dataframe
    coef_values = results_df['coef'].values
    
    assert np.allclose(coef_values[0], 0, atol=0.01)
    assert np.allclose(coef_values[1], 1, atol=0.01)


def test_target_col(sample_data, temp_dirs):
    """Test that function raises error when target column doesn't exist."""
    model_dir, table_dir = temp_dirs
    
    with pytest.raises(KeyError):
        lin_reg(sample_data, 'nonexistent_target', model_dir, 
               "model.pickle", table_dir, "table.csv")


def test_pickle_name(sample_data, temp_dirs):
    """Test that function raises error when model_name doesn't end with .pickle."""
    model_dir, table_dir = temp_dirs
    
    with pytest.raises(ValueError, match=".*pickle"):
        lin_reg(sample_data, 'target', model_dir, 
               "model.txt", table_dir, "table.csv")


def test_csv_name(sample_data, temp_dirs):
    """Test that function raises error when table_name doesn't end with .csv."""
    model_dir, table_dir = temp_dirs
    
    with pytest.raises(ValueError, match=".*csv"):
        lin_reg(sample_data, 'target', model_dir, 
               "model.pickle", table_dir, "table.txt")


def test_model_dir(sample_data, temp_dirs):
    """Test that function raises error when model_dir doesn't exist."""
    _, table_dir = temp_dirs
    nonexistent_dir = "/nonexistent/path/to/model"
    
    with pytest.raises(FileNotFoundError):
        lin_reg(sample_data, 'target', nonexistent_dir, 
               "model.pickle", table_dir, "table.csv")


def test_table_dir(sample_data, temp_dirs):
    """Test that function raises error when table_dir doesn't exist."""
    model_dir, _ = temp_dirs
    nonexistent_dir = "/nonexistent/path/to/table"
    
    with pytest.raises(FileNotFoundError):
        lin_reg(sample_data, 'target', model_dir, 
               "model.pickle", nonexistent_dir, "table.csv")


def test_pg_error(sample_data, temp_dirs):
    """Test that function propagates errors from pg.linear_regression."""
    model_dir, table_dir = temp_dirs
    
    with patch('src.lin_reg.pg.linear_regression') as mock_lr:
        mock_lr.side_effect = ValueError("Singular matrix error")
        
        with pytest.raises(ValueError, match="Singular matrix error"):
            lin_reg(sample_data, 'target', model_dir, 
                   "model.pickle", table_dir, "table.csv")
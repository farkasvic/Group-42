
import os
import sys
import pytest
import tempfile

# Add the src directory to the path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from check_csv import check_csv

@pytest.fixture
def test_data_dir():
    """Fixture to provide the test data directory path."""
    return os.path.dirname(__file__)

# testing for simple expected use cases

def test_valid_csv_file_correct_name_and_extension(test_data_dir):
    """Test that a valid CSV file with correct name and extension passes validation."""
    filepath = os.path.join(test_data_dir, 'clean_diabetes.csv')
    check_csv(filepath, 'clean_diabetes.csv', '.csv')

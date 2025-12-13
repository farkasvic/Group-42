
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

# testing for edge cases
def test_uppercase_extension():
    """Test validation with uppercase extension (case sensitivity)."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.CSV', delete=False) as f:
        f.write("data\n")
        temp_path = f.name

    try:
        expected_filename = os.path.basename(temp_path)

        # Should pass with correct uppercase extension
        check_csv(temp_path, expected_filename, '.CSV')

        # Should fail if we expect lowercase but file has uppercase
        with pytest.raises(AssertionError, match="Expected file extension '.csv'"):
            check_csv(temp_path, expected_filename, '.csv')
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def test_file_without_extension():
    """Test validation with file that has no extension."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='', delete=False) as f:
        f.write("data\n")
        temp_path = f.name
    try:
        expected_filename = os.path.basename(temp_path)
        check_csv(temp_path, expected_filename, '')
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

# testing for abnormal / error use cases

def test_wrong_filename(test_data_dir):
    """Test that function raises AssertionError when filename doesn't match."""
    filepath = os.path.join(test_data_dir, 'clean_diabetes.csv')
    with pytest.raises(AssertionError, match="Expected filename 'wrong_name.csv'"):
        check_csv(filepath, 'wrong_name.csv', '.csv')

def test_wrong_extension(test_data_dir):
    """Test that function raises AssertionError when extension doesn't match."""
    filepath = os.path.join(test_data_dir, 'clean_diabetes.csv')
    with pytest.raises(AssertionError, match="Expected file extension '.txt'"):
        check_csv(filepath, 'clean_diabetes.csv', '.txt')

def test_both_filename_and_extension_wrong(test_data_dir):
    """Test with both filename and extension incorrect."""
    filepath = os.path.join(test_data_dir, 'clean_diabetes.csv')
    with pytest.raises(AssertionError, match="Expected filename"):
        check_csv(filepath, 'wrong_file.txt', '.txt')

def test_empty_string_filepath():
    """Test with empty string as filepath."""
    with pytest.raises(AssertionError):
        check_csv('', 'file.csv', '.csv')

def test_case_sensitivity_filename(test_data_dir):
    """Test case sensitivity for filename validation."""
    filepath = os.path.join(test_data_dir, 'clean_diabetes.csv')
    with pytest.raises(AssertionError, match="Expected filename 'Clean_Diabetes.csv'"):
        check_csv(filepath, 'Clean_Diabetes.csv', '.csv')

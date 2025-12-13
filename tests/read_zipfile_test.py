import pytest
import os
import shutil
from unittest.mock import patch, Mock
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.read_zipfile import read_zipfile
from tests.generate_test_files import create_simple_zip, create_multi_file_zip

if not os.path.exists('tests/test_data'):
    os.makedirs('tests/test_data')


# Test 1: basic functionality
def test_basic_download():
    """Test that the function can download and extract a .dat file"""
    test_dir = 'tests/test_data'
    url = 'http://example.com/test.zip'
    
    # make a fake zip file
    fake_zip = create_simple_zip()
    
    # mock the requests.get call
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.content = fake_zip
        mock_get.return_value = mock_response
        
        # run the function
        read_zipfile(url, test_dir)
        
        # check the file exists
        assert os.path.exists(os.path.join(test_dir, 'data.dat'))
        
        # check content is right
        with open(os.path.join(test_dir, 'data.dat'), 'r') as f:
            content = f.read()
        assert content == "Sample data content"
    
    # cleanup
    if os.path.exists(os.path.join(test_dir, 'data.dat')):
        os.remove(os.path.join(test_dir, 'data.dat'))


# Test 2: only extracts .dat file
def test_only_extracts_dat():
    """Test that only the .dat file is extracted from a zip with multiple files"""
    test_dir = 'tests/test_data'
    url = 'http://example.com/multi.zip'
    
    fake_zip = create_multi_file_zip()
    
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.content = fake_zip
        mock_get.return_value = mock_response
        
        read_zipfile(url, test_dir)
        
        # .dat file should exist
        assert os.path.exists(os.path.join(test_dir, 'data.dat'))
        
        # other files should NOT exist
        assert not os.path.exists(os.path.join(test_dir, 'readme.txt'))
        assert not os.path.exists(os.path.join(test_dir, 'metadata.json'))
    
    # cleanup
    if os.path.exists(os.path.join(test_dir, 'data.dat')):
        os.remove(os.path.join(test_dir, 'data.dat'))


# Test 3: creates directory if it doesn't exist
def test_creates_directory():
    """Test that function creates the directory if it doesn't exist"""
    test_dir = 'tests/new_test_dir'
    url = 'http://example.com/test.zip'
    
    # make sure directory doesn't exist
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
    fake_zip = create_simple_zip()
    
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.content = fake_zip
        mock_get.return_value = mock_response
        
        read_zipfile(url, test_dir)
        
        # directory should be created
        assert os.path.exists(test_dir)
        assert os.path.isdir(test_dir)
    
    # cleanup
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)


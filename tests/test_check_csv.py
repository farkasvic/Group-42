
import os
import sys
import pytest
import tempfile

# Add the src directory to the path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from check_csv import check_csv

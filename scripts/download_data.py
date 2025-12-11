"""
Script to download and extract diabetes dataset from a remote URL.
"""
import click
import os
from src.read_zipfile import read_zipfile

@click.command()
@click.option('--url', type=str, default='https://sci2s.ugr.es/keel/dataset/data/regression/diabetes.zip',
              help='URL to download the dataset from'
)
@click.option('--data-dir', type=str, default='data/raw', help='Directory to store downloaded and processed data')


def main(url, data_dir):
    """
    Download and extract diabetes dataset from remote URL.
    
    Downloads the zip file from the specified URL, saves it to the data directory,
    and extracts the .dat file contained within.
    """

    try:
        read_zipfile(url, data_dir)
    except:
        os.makedirs(data_dir)
        read_zipfile(url, data_dir)


if __name__ == '__main__':
    main()
"""
IconLib: A Python module for accessing and managing Constitution data.
This module provides functionality to retrieve articles, search keywords, 
list articles, and much more from a JSON file containing Constitution data.
"""

from os.path import abspath, join, dirname
from typing import List, Dict
import json

__title__ = 'IconLib'
__version__ = '1.0'
__author__ = 'Vikhram S'
__license__ = 'Apache License 2.0'


def _path_to(file: str) -> str:
    """
    Generate the absolute path to a given file within the package directory.
    :param file: File name or relative path.
    :return: Absolute path to the file.
    """
    return abspath(join(dirname(__file__), file))


class IconLib:
    def __init__(self, data_file: str = 'constitution_of_india.json'):
        """
        Initialize the IconLib class and load the Constitution data.
        :param data_file: Path to the JSON file containing the data.
        """
        self.data = self._load_data(_path_to(data_file))

    @staticmethod
    def _load_data(file_path: str) -> List[Dict]:
        """
        Load Constitution data from the JSON file.
        :param file_path: Path to the JSON file.
        :return: List of data dictionaries from the file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in the file.")

    # Add your methods here (e.g., preamble, get_article, etc.)
    # ...

__all__ = ['IconLib']

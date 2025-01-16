"""
IconLib: A Python module for accessing and managing Constitution data.
This module provides functionality to retrieve articles, search keywords, 
list articles, and much more from a JSON file containing Constitution data.
"""

from .iconlib import IconLib

__title__ = 'IconLib'
__version__ = '1.0'
__author__ = 'Vikhram S'
__license__ = 'Apache License 2.0'

# Exported symbols for top-level import
__all__ = [
    'IconLib',
    'get_preamble',
    'get_article',
    'list_articles',
    'search_keyword',
    'get_article_summary',
    'count_total_articles',
    'search_by_title',
]

# Functions for easier direct usage
def get_preamble(iconlib_instance: IconLib) -> str:
    """Retrieve the Preamble of the Constitution."""
    return iconlib_instance.preamble()

def get_article(iconlib_instance: IconLib, number: int) -> str:
    """Retrieve the details of a specific article."""
    return iconlib_instance.get_article(number)

def list_articles(iconlib_instance: IconLib) -> str:
    """List all articles in the Constitution."""
    return iconlib_instance.articles_list()

def search_keyword(iconlib_instance: IconLib, keyword: str) -> str:
    """Search for a keyword in the Constitution."""
    return iconlib_instance.search_keyword(keyword)

def get_article_summary(iconlib_instance: IconLib, number: int) -> str:
    """Provide a brief summary of the specified article."""
    return iconlib_instance.article_summary(number)

def count_total_articles(iconlib_instance: IconLib) -> int:
    """Count the total number of articles in the Constitution."""
    return iconlib_instance.count_articles()

def search_by_title(iconlib_instance: IconLib, title_keyword: str) -> str:
    """Search for articles by title keyword."""
    return iconlib_instance.search_by_title(title_keyword)

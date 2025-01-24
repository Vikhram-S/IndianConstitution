"""
IndianConstitution: A Python module for accessing and managing Constitution data.
This module provides functionality to retrieve articles, search keywords, 
list articles, and much more from a JSON file containing Constitution data.
"""

from .indianconstitution import IndianConstitution

__title__ = 'IndianConstitution'
__version__ = '0.5.2'
__author__ = 'Vikhram S'
__license__ = 'Apache License 2.0'

# Exported symbols for top-level import
__all__ = [
    'IndianConstitution',
    'get_preamble',
    'get_article',
    'list_articles',
    'search_keyword',
    'get_article_summary',
    'count_total_articles',
    'search_by_title',
]

# Functions for easier direct usage
def get_preamble(indianconst_instance: IndianConstitution) -> str:
    """Retrieve the Preamble of the Constitution."""
    return indianconst_instance.preamble()

def get_article(indianconst_instance: IndianConstitution, number: int) -> str:
    """Retrieve the details of a specific article."""
    return indianconst_instance.get_article(number)

def list_articles(indianconst_instance: IndianConstitution) -> str:
    """List all articles in the Constitution."""
    return indianconst_instance.articles_list()

def search_keyword(indianconst_instance: IndianConstitution, keyword: str) -> str:
    """Search for a keyword in the Constitution."""
    return indianconst_instance.search_keyword(keyword)

def get_article_summary(indianconst_instance: IndianConstitution, number: int) -> str:
    """Provide a brief summary of the specified article."""
    return indianconst_instance.article_summary(number)

def count_total_articles(indianconst_instance: IndianConstitution) -> int:
    """Count the total number of articles in the Constitution."""
    return indianconst_instance.count_articles()

def search_by_title(indianconst_instance: IndianConstitution, title_keyword: str) -> str:
    """Search for articles by title keyword."""
    return indianconst_instance.search_by_title(title_keyword)
